import re
from PySide6.QtWidgets import QWidget,QFormLayout,QLineEdit,QCheckBox,QSpinBox,QPushButton,QLabel,QHBoxLayout
from ..models.generation_settings import FilterSettings
class FiltersPage(QWidget):
    def __init__(self):
        super().__init__(); f=QFormLayout(self); self.enable=QCheckBox('Enable filters'); f.addRow(self.enable); self.start=QLineEdit(); self.end=QLineEdit(); self.contains=QLineEdit(); self.not_contains=QLineEdit(); self.regex=QLineEdit()
        self.mind=QSpinBox(); self.minl=QSpinBox(); self.minu=QSpinBox(); self.minlo=QSpinBox(); self.mins=QSpinBox(); self.max_repeat=QSpinBox(); self.max_repeat.setSpecialValueText('Disabled'); self.adj=QCheckBox('Disallow adjacent repeated characters')
        for lab,w in [('Must start with',self.start),('Must end with',self.end),('Must contain',self.contains),('Must not contain',self.not_contains),('Min digits',self.mind),('Min letters',self.minl),('Min uppercase',self.minu),('Min lowercase',self.minlo),('Min symbols',self.mins),('Max occurrence of one char',self.max_repeat),('Adjacent repeats',self.adj),('Regular expression',self.regex)]: f.addRow(lab,w)
        self.status=QLabel('Regex not validated'); val=QPushButton('Validate regex'); reset=QPushButton('Reset filters'); row=QHBoxLayout(); row.addWidget(val); row.addWidget(reset); row.addWidget(self.status); f.addRow(row); f.addRow(QLabel('Filtering can greatly reduce output but may still evaluate many candidates.'))
        val.clicked.connect(self.validate_regex); reset.clicked.connect(self.reset)
    def validate_regex(self):
        try: re.compile(self.regex.text()) if self.regex.text() else None; self.status.setText('Regex valid')
        except re.error as e: self.status.setText(f'Regex invalid: {e}')
    def reset(self):
        for w in (self.start,self.end,self.contains,self.not_contains,self.regex): w.clear()
        for w in (self.mind,self.minl,self.minu,self.minlo,self.mins,self.max_repeat): w.setValue(0)
        self.adj.setChecked(False); self.enable.setChecked(False); self.status.setText('Regex not validated')
    def to_settings(self):
        if not self.enable.isChecked(): return FilterSettings()
        if self.regex.text(): re.compile(self.regex.text())
        return FilterSettings(self.start.text(),self.end.text(),self.contains.text(),self.not_contains.text(),self.mind.value(),self.minl.value(),self.minu.value(),self.minlo.value(),self.mins.value(),self.adj.isChecked(),self.max_repeat.value() or None,self.regex.text())
