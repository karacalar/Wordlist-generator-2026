from __future__ import annotations
import logging, time, threading, traceback
from dataclasses import dataclass
from pathlib import Path
try:
    from PySide6.QtCore import QObject, Signal, Slot
except ModuleNotFoundError:  # allows headless core tests when Qt is unavailable
    class _Signal:
        def __init__(self,*a,**k): self._slots=[]
        def connect(self, fn): self._slots.append(fn)
        def emit(self,*a,**k):
            for fn in list(self._slots): fn(*a,**k)
    class QObject:
        def __init__(self, *args, **kwargs):
            super().__init__()
    def Signal(*a,**k): return _Signal()
    def Slot(*a,**k):
        def deco(fn): return fn
        return deco
from ..models.enums import GenerationMode
from ..generation.cartesian_generator import generate_fixed, generate_range, generate_product_from_sets
from ..generation.counter_generator import generate_counter, counter_count
from ..generation.random_generator import generate_random_unique
from ..generation.template_generator import template_to_position_sets
from ..generation.filters import OutputFilter
from ..generation.preview import theoretical_total
from ..output.file_splitter import FileSplitter
from ..output.manifest import write_manifest
from ..utils.disk_space import ensure_space

log = logging.getLogger(__name__)

@dataclass
class Progress:
    records:int; total:int; bytes_written:int; current_file:str; elapsed:float; rate:float; eta:float; index:int; status:str

def _iter_base(settings):
    s=settings; cs=s.charset.build()
    if not cs and s.mode not in (GenerationMode.PATTERN, GenerationMode.TEMPLATE, GenerationMode.COUNTER):
        raise ValueError("Character set cannot be empty.")
    if s.mode in (GenerationMode.FIXED, GenerationMode.PREFIX_SUFFIX): return generate_fixed(cs,s.exact_length,s.start_index,s.end_index)
    if s.mode==GenerationMode.RANGE: return generate_range(cs,s.min_length,s.max_length,s.start_index,s.end_index)
    if s.mode==GenerationMode.PATTERN: return generate_product_from_sets(s.position_sets,s.start_index,s.end_index)
    if s.mode==GenerationMode.TEMPLATE: return generate_product_from_sets(template_to_position_sets(s.template,s.custom_tokens),s.start_index,s.end_index)
    if s.mode==GenerationMode.COUNTER: return generate_counter(s.counter_start,s.counter_end,s.counter_step,s.counter_padding,"","")
    return generate_random_unique(cs,s.exact_length,s.random_count,s.secure_random)

def iter_generated_values(settings):
    for idx, val in _iter_base(settings):
        for p in (settings.prefixes or [""]):
            for suf in (settings.suffixes or [""]):
                yield idx, f"{p}{val}{suf}", p, suf

class GenerationWorker(QObject):
    progress = Signal(object)
    completed = Signal(dict)
    failed = Signal(str)
    stopped = Signal(dict)
    paused = Signal()
    resumed = Signal()

    def __init__(self, settings, estimated_bytes: int = 0, safety_margin_bytes: int = 0):
        super().__init__(); self.settings=settings; self.estimated_bytes=estimated_bytes; self.safety_margin_bytes=safety_margin_bytes
        self._stop=threading.Event(); self._pause=threading.Event(); self._resume_gate=threading.Event(); self._resume_gate.set()

    def stop(self): self._stop.set(); self._resume_gate.set()
    def pause(self): self._pause.set(); self._resume_gate.clear(); self.paused.emit()
    def resume(self): self._pause.clear(); self._resume_gate.set(); self.resumed.emit()

    @Slot()
    def run(self):
        s=self.settings; out=s.output; start_time=time.monotonic(); records=0; last=-1; status='completed'
        try:
            out.directory.mkdir(parents=True,exist_ok=True)
            ensure_space(out.directory,self.estimated_bytes,self.safety_margin_bytes)
            filt=OutputFilter(s.filters)
            total=theoretical_total(s)
            splitter=FileSplitter(out.directory,out.base_name,str(out.format),out.max_records_per_file,out.max_bytes_per_file,newline=str(out.newline),bom=out.utf8_bom,csv_columns=out.csv_columns,buffer_size=out.buffer_size)
            last_emit=0.0
            try:
                for idx, full, p, suf in iter_generated_values(s):
                    if self._stop.is_set(): status='interrupted'; break
                    while self._pause.is_set() and not self._stop.is_set(): self._resume_gate.wait(0.1)
                    if self._stop.is_set(): status='interrupted'; break
                    if filt.match(full):
                        splitter.write(idx,full,p,suf); records+=1; last=idx
                    if records >= s.max_records: status='completed_limit'; break
                    now=time.monotonic()
                    if now-last_emit >= 0.15:
                        bw=sum(w.bytes_written for w in splitter.files); rate=records/max(now-start_time,0.001); eta=(max(total-records,0)/rate) if rate else 0
                        self.progress.emit(Progress(records,total,bw,str(splitter.current.path if splitter.current else ''),now-start_time,rate,eta,idx,'running'))
                        last_emit=now
            finally:
                splitter.close()
            files=[w.path for w in splitter.files]
            manifest=write_manifest(out.directory,s,total,[s.start_index,last],records,status,files)
            result={"records":records,"status":status,"manifest":manifest,"files":files,"total":total}
            if status=='interrupted': self.stopped.emit(result)
            else: self.completed.emit(result)
            return result
        except Exception as exc:
            log.exception("Generation failed")
            self.failed.emit(f"{exc}\n\n{traceback.format_exc()}")
            raise
