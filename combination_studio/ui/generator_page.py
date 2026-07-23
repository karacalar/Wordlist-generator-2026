from PySide6.QtWidgets import QWidget,QVBoxLayout,QFormLayout,QComboBox,QLineEdit,QSpinBox,QCheckBox,QPushButton,QTextEdit,QLabel,QHBoxLayout
from ..models.character_set import GROUPS, CharacterSetSpec
from ..generation.estimator import estimate_uniform
class GeneratorPage(QWidget):
    def __init__(self):
        super().__init__(); root=QVBoxLayout(self); form=QFormLayout(); root.addLayout(form)
        self.mode=QComboBox(); self.mode.addItems(['Fixed Length','Length Range','Prefix/Suffix','Position Pattern','Template','Counter','Random Unique']); form.addRow('Generation mode',self.mode)
        self.checks=[]
        for name in GROUPS:
            cb=QCheckBox(name); self.checks.append(cb); form.addRow(cb)
        self.checks[0].setChecked(True); self.custom=QLineEdit(); self.exclude=QLineEdit(); self.length=QSpinBox(); self.length.setRange(1,64); self.length.setValue(5); self.min_len=QSpinBox(); self.min_len.setRange(1,64); self.max_len=QSpinBox(); self.max_len.setRange(1,64); self.max_records=QSpinBox(); self.max_records.setRange(1,10000000); self.max_records.setValue(10000000)
        form.addRow('Custom character set',self.custom); form.addRow('Exclude characters',self.exclude); form.addRow('Exact length',self.length); form.addRow('Minimum length',self.min_len); form.addRow('Maximum length',self.max_len); form.addRow('Maximum records',self.max_records)
        self.info=QLabel(); root.addWidget(self.info); self.preview=QTextEdit(); self.preview.setReadOnly(True); root.addWidget(self.preview)
        row=QHBoxLayout(); root.addLayout(row)
        for t in ['Preview','Start Generation','Pause','Resume','Stop','Open Output Folder']:
            b=QPushButton(t); row.addWidget(b); b.clicked.connect(self.update_info)
        for w in [*self.checks,self.custom,self.exclude,self.length]:
            try: w.stateChanged.connect(self.update_info)
            except Exception: w.textChanged.connect(self.update_info)
        self.update_info()
    def charset(self): return CharacterSetSpec([cb.text() for cb in self.checks if cb.isChecked()],self.custom.text(),self.exclude.text()).build()
    def update_info(self):
        cs=self.charset(); self.info.setText(f'Active character set ({len(cs)}): {cs}\nLive combination count and feasibility are calculated before generation.')
        if cs:
            est=estimate_uniform(len(cs),self.length.value()); self.preview.setPlainText(f'Total: {est.total:,}\nScientific: {est.total:.14e}\nEstimated bytes: {est.estimated_bytes:,}\nAvailable disk: {est.available_bytes:,}\nFeasible: {est.feasible}')
