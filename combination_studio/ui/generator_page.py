import logging, time
from pathlib import Path
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget,QVBoxLayout,QFormLayout,QComboBox,QLineEdit,QSpinBox,QCheckBox,QPushButton,QTextEdit,QLabel,QHBoxLayout,QGridLayout,QGroupBox,QMessageBox,QProgressBar,QDialog
from ..models.character_set import GROUPS, CharacterSetSpec
from ..models.enums import GenerationMode
from ..models.generation_settings import GenerationSettings
from ..generation.estimator import estimate_uniform
from ..generation.preview import preview_values, theoretical_total
from ..jobs.worker import GenerationWorker
log=logging.getLogger(__name__)
LABELS={'digits':'Digits (0-9)','lower':'Lowercase letters (a-z)','upper':'Uppercase letters (A-Z)','lower_upper':'Lowercase + uppercase','letters_digits':'Letters + digits','letters_digits_safe_symbols':'Letters, digits + safe symbols','hex_lower':'Hexadecimal lowercase','hex_upper':'Hexadecimal uppercase','binary':'Binary','turkish_lower':'Turkish lowercase','turkish_upper':'Turkish uppercase'}
class GeneratorPage(QWidget):
    def __init__(self, pattern_page=None, prefix_suffix_page=None, filters_page=None, output_page=None, settings_page=None):
        super().__init__(); self.pattern_page=pattern_page; self.prefix_suffix_page=prefix_suffix_page; self.filters_page=filters_page; self.output_page=output_page; self.settings_page=settings_page; self.thread=None; self.worker=None
        root=QVBoxLayout(self); root.setContentsMargins(12,12,12,12)
        top=QHBoxLayout(); root.addLayout(top)
        settings_box=QGroupBox('Generation settings'); form=QFormLayout(settings_box); top.addWidget(settings_box,2)
        self.mode=QComboBox(); self.mode.addItems(['Fixed Length','Length Range','Prefix/Suffix','Position Pattern','Template','Counter','Random Unique']); form.addRow('Generation mode',self.mode)
        grid=QGridLayout(); self.checks={}
        for i,name in enumerate(GROUPS):
            cb=QCheckBox(LABELS[name]); cb.setProperty('group_key',name); self.checks[name]=cb; grid.addWidget(cb,i//2,i%2)
        self.checks['digits'].setChecked(True); form.addRow('Character groups',grid)
        self.custom=QLineEdit(); self.exclude=QLineEdit(); self.length=QSpinBox(); self.length.setRange(1,64); self.length.setValue(5); self.min_len=QSpinBox(); self.min_len.setRange(1,64); self.min_len.setValue(1); self.max_len=QSpinBox(); self.max_len.setRange(1,64); self.max_len.setValue(5); self.max_records=QSpinBox(); self.max_records.setRange(1,100000000); self.max_records.setValue(10000000)
        for label,w in [('Custom character set',self.custom),('Exclude characters',self.exclude),('Exact length',self.length),('Minimum length',self.min_len),('Maximum length',self.max_len),('Maximum records',self.max_records)]: form.addRow(label,w)
        self.info=QLabel(); self.info.setWordWrap(True); top.addWidget(self.info,1)
        self.preview_box=QTextEdit(); self.preview_box.setReadOnly(True); self.preview_box.setMaximumHeight(160); root.addWidget(self.preview_box)
        prog=QGroupBox('Progress'); pf=QFormLayout(prog); self.progress=QProgressBar(); self.progress.setRange(0,10000); self.records=QLabel('0 / 0'); self.bytes=QLabel('0'); self.file=QLabel('-'); self.elapsed=QLabel('0s'); self.rate=QLabel('0/s'); self.eta=QLabel('-'); self.status=QLabel('Idle')
        for lab,w in [('Progress',self.progress),('Records',self.records),('Bytes written',self.bytes),('Current file',self.file),('Elapsed',self.elapsed),('Rate',self.rate),('ETA',self.eta),('Status',self.status)]: pf.addRow(lab,w)
        root.addWidget(prog)
        row=QHBoxLayout(); root.addLayout(row); self.preview_button=QPushButton('Preview'); self.start_button=QPushButton('Start Generation'); self.pause_button=QPushButton('Pause'); self.resume_button=QPushButton('Resume'); self.stop_button=QPushButton('Stop'); self.open_button=QPushButton('Open Output Folder')
        for b in [self.preview_button,self.start_button,self.pause_button,self.resume_button,self.stop_button,self.open_button]: row.addWidget(b)
        self.preview_button.clicked.connect(self.show_preview); self.start_button.clicked.connect(self.start_generation); self.pause_button.clicked.connect(self.pause_generation); self.resume_button.clicked.connect(self.resume_generation); self.stop_button.clicked.connect(self.stop_generation); self.open_button.clicked.connect(self.open_output_folder)
        for w in [*self.checks.values(),self.custom,self.exclude,self.length,self.min_len,self.max_len,self.mode]:
            sig=getattr(w,'stateChanged',None) or getattr(w,'textChanged',None) or getattr(w,'currentIndexChanged',None); sig.connect(self.update_info)
        self.set_idle(); self.update_info()
    def charset(self): return CharacterSetSpec([k for k,c in self.checks.items() if c.isChecked()],self.custom.text(),self.exclude.text()).build()
    def build_settings(self):
        mode=[GenerationMode.FIXED,GenerationMode.RANGE,GenerationMode.PREFIX_SUFFIX,GenerationMode.PATTERN,GenerationMode.TEMPLATE,GenerationMode.COUNTER,GenerationMode.RANDOM_UNIQUE][self.mode.currentIndex()]
        out=self.output_page.to_settings() if self.output_page else None; filters=self.filters_page.to_settings() if self.filters_page else None
        s=GenerationSettings(mode=mode,charset=CharacterSetSpec([k for k,c in self.checks.items() if c.isChecked()],self.custom.text(),self.exclude.text()),exact_length=self.length.value(),min_length=self.min_len.value(),max_length=self.max_len.value(),max_records=self.max_records.value())
        if out: s.output=out
        if filters: s.filters=filters
        if self.prefix_suffix_page: s.prefixes=self.prefix_suffix_page.get_prefixes(); s.suffixes=self.prefix_suffix_page.get_suffixes()
        if self.pattern_page and mode==GenerationMode.PATTERN: s.position_sets=self.pattern_page.position_sets()
        return s
    def validate_settings(self):
        s=self.build_settings();
        if s.min_length>s.max_length: raise ValueError('Minimum length cannot exceed maximum length.')
        if s.mode!=GenerationMode.PATTERN and not s.charset.build(): raise ValueError('Select at least one character or enter a custom character set.')
        total=theoretical_total(s)
        if total>s.hard_safety_limit: raise ValueError(f'Theoretical total {total:,} exceeds hard safety limit {s.hard_safety_limit:,}.')
        return s,total
    def update_info(self):
        try:
            s=self.build_settings(); cs=s.charset.build(); total=theoretical_total(s); est=estimate_uniform(max(len(cs),1),s.exact_length,prefixes=s.prefixes,suffixes=s.suffixes,available_path=s.output.directory,max_records_per_file=s.output.max_records_per_file)
            self.info.setText(f'Active character set ({len(cs)}): {cs}\nTotal theoretical records: {total:,} ({total:.14e})\nEstimated bytes: {est.estimated_bytes:,}\nAvailable disk: {est.available_bytes:,}\nFeasible: {est.feasible}')
        except Exception as e: self.info.setText(f'Configuration warning: {e}')
    def show_preview(self):
        try:
            s,total=self.validate_settings(); limit=self.settings_page.preview_limit.value() if self.settings_page else 100; vals=preview_values(s,limit=limit); self.preview_box.setPlainText(f'Total theoretical records: {total:,}\nPreview ({len(vals)} records):\n'+'\n'.join(vals))
        except Exception as e: log.exception('Preview failed'); QMessageBox.warning(self,'Preview failed',str(e))
    def start_generation(self):
        if self.thread: QMessageBox.warning(self,'Generation running','A job is already running.'); return
        try:
            s,total=self.validate_settings(); estimated=estimate_uniform(max(len(s.charset.build()),1),s.exact_length,prefixes=s.prefixes,suffixes=s.suffixes,available_path=s.output.directory).estimated_bytes
            self.thread=QThread(self); self.worker=GenerationWorker(s,estimated,self.settings_page.margin.value() if self.settings_page else 0); self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.on_progress); self.worker.completed.connect(self.on_completed); self.worker.stopped.connect(self.on_stopped); self.worker.failed.connect(self.on_failed)
            self.worker.completed.connect(self.thread.quit); self.worker.stopped.connect(self.thread.quit); self.worker.failed.connect(self.thread.quit); self.thread.finished.connect(self.thread.deleteLater); self.thread.finished.connect(self.cleanup_thread)
            self.set_running(); self.thread.start()
        except Exception as e: log.exception('Could not start generation'); QMessageBox.critical(self,'Could not start generation',str(e)); self.set_idle()
    def pause_generation(self):
        if self.worker: self.worker.pause(); self.set_paused(); self.status.setText('Paused')
    def resume_generation(self):
        if self.worker: self.worker.resume(); self.set_running(); self.status.setText('Running')
    def stop_generation(self):
        if self.worker: self.worker.stop(); self.status.setText('Stopping...')
    def open_output_folder(self):
        if self.output_page:
            self.output_page.open_folder()

    def on_progress(self,p):
        self.progress.setValue(int((p.records/max(p.total,1))*10000)); self.records.setText(f'{p.records:,} / {p.total:,}'); self.bytes.setText(f'{p.bytes_written:,}'); self.file.setText(p.current_file); self.elapsed.setText(f'{p.elapsed:.1f}s'); self.rate.setText(f'{p.rate:.0f}/s'); self.eta.setText(f'{p.eta:.1f}s'); self.status.setText(p.status)
    def on_completed(self,r): self.status.setText(f"Completed: {r['records']:,} records"); self.set_idle(); QMessageBox.information(self,'Generation complete',f"Wrote {r['records']:,} records.\nManifest: {r['manifest']}")
    def on_stopped(self,r): self.status.setText(f"Stopped: {r['records']:,} records"); self.set_idle(); QMessageBox.warning(self,'Generation stopped',f"Partial output saved.\nManifest: {r['manifest']}")
    def on_failed(self,msg): self.status.setText('Failed'); self.set_idle(); QMessageBox.critical(self,'Generation failed',msg)
    def cleanup_thread(self): self.thread=None; self.worker=None
    def set_idle(self): self.start_button.setEnabled(True); self.preview_button.setEnabled(True); self.pause_button.setEnabled(False); self.resume_button.setEnabled(False); self.stop_button.setEnabled(False)
    def set_running(self): self.start_button.setEnabled(False); self.preview_button.setEnabled(False); self.pause_button.setEnabled(True); self.resume_button.setEnabled(False); self.stop_button.setEnabled(True); self.status.setText('Running')
    def set_paused(self): self.pause_button.setEnabled(False); self.resume_button.setEnabled(True); self.stop_button.setEnabled(True)
