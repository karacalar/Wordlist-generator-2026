from pathlib import Path
from ..models.enums import GenerationMode
from ..generation.cartesian_generator import generate_fixed, generate_range, generate_product_from_sets
from ..generation.pattern_generator import parse_position_pattern
from ..generation.counter_generator import generate_counter, counter_count
from ..generation.random_generator import generate_random_unique
from ..generation.template_generator import template_to_position_sets
from ..generation.filters import OutputFilter
from ..output.file_splitter import FileSplitter
from ..output.manifest import write_manifest
from ..utils.disk_space import ensure_space
class GenerationWorker:
    def __init__(self,settings): self.settings=settings; self.stop_requested=False; self.pause_requested=False
    def stop(self): self.stop_requested=True
    def _base_iter(self):
        s=self.settings; cs=s.charset.build()
        if s.mode==GenerationMode.FIXED or s.mode==GenerationMode.PREFIX_SUFFIX: return generate_fixed(cs,s.exact_length,s.start_index,s.end_index), len(cs)**s.exact_length
        if s.mode==GenerationMode.RANGE: return generate_range(cs,s.min_length,s.max_length,s.start_index,s.end_index), sum(len(cs)**n for n in range(s.min_length,s.max_length+1))
        if s.mode==GenerationMode.PATTERN: return generate_product_from_sets(s.position_sets,s.start_index,s.end_index), __import__('math').prod(map(len,s.position_sets))
        if s.mode==GenerationMode.TEMPLATE:
            sets=template_to_position_sets(s.template,s.custom_tokens); return generate_product_from_sets(sets,s.start_index,s.end_index), __import__('math').prod(map(len,sets))
        if s.mode==GenerationMode.COUNTER: return generate_counter(s.counter_start,s.counter_end,s.counter_step,s.counter_padding,s.prefixes[0] if s.prefixes else "",s.suffixes[0] if s.suffixes else ""), counter_count(s.counter_start,s.counter_end,s.counter_step)
        return generate_random_unique(cs,s.exact_length,s.random_count,s.secure_random), s.random_count
    def run(self):
        s=self.settings; out=s.output; out.directory.mkdir(parents=True,exist_ok=True); filt=OutputFilter(s.filters); it,total=self._base_iter(); ensure_space(out.directory,0,0)
        splitter=FileSplitter(out.directory,out.base_name,str(out.format),out.max_records_per_file,out.max_bytes_per_file,newline=str(out.newline),bom=out.utf8_bom,csv_columns=out.csv_columns,buffer_size=out.buffer_size)
        records=0; last=-1; status='completed'
        try:
            for idx,val in it:
                if self.stop_requested: status='interrupted'; break
                for p in s.prefixes:
                    for suf in s.suffixes:
                        full=f"{p}{val}{suf}"
                        if filt.match(full): splitter.write(idx,full,p,suf); records+=1; last=idx
                        if records>=s.max_records: status='completed_limit'; raise StopIteration
        except StopIteration: pass
        finally: splitter.close()
        files=[w.path for w in splitter.files]; manifest=write_manifest(out.directory,s,total,[s.start_index,last],records,status,files)
        return {"records":records,"status":status,"manifest":manifest,"files":files}
