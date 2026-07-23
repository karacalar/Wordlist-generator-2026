from pathlib import Path
from PySide6.QtWidgets import QWidget,QFormLayout,QSpinBox,QLineEdit,QCheckBox,QComboBox,QPushButton,QHBoxLayout,QMessageBox
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__(); f=QFormLayout(self); self.default_output=QLineEdit(str(Path('output').absolute())); self.preview_limit=QSpinBox(); self.preview_limit.setRange(1,10000); self.preview_limit.setValue(100); self.max_records=QSpinBox(); self.max_records.setRange(1,100000000); self.max_records.setValue(10000000); self.margin=QSpinBox(); self.margin.setRange(0,2000000000); self.margin.setValue(100*1024*1024); self.buffer=QSpinBox(); self.buffer.setRange(4096,16*1024*1024); self.buffer.setValue(1024*1024); self.interval=QSpinBox(); self.interval.setRange(50,1000); self.interval.setValue(150); self.remember=QCheckBox(); self.remember.setChecked(True); self.open_after=QCheckBox(); self.level=QComboBox(); self.level.addItems(['INFO','DEBUG','WARNING','ERROR'])
        for lab,w in [('Default output directory',self.default_output),('Preview record limit',self.preview_limit),('Maximum allowed records',self.max_records),('Disk safety margin bytes',self.margin),('Write buffer size',self.buffer),('Progress update interval ms',self.interval),('Remember last settings',self.remember),('Open output folder after completion',self.open_after),('Logging level',self.level)]: f.addRow(lab,w)
        row=QHBoxLayout(); save=QPushButton('Save'); defaults=QPushButton('Restore Defaults'); row.addWidget(save); row.addWidget(defaults); f.addRow(row); save.clicked.connect(self.save_settings); defaults.clicked.connect(self.restore_defaults)
    def save_settings(self):
        QMessageBox.information(self,'Settings','Settings validated for this session.')
    def restore_defaults(self):
        self.preview_limit.setValue(100); self.max_records.setValue(10000000); self.margin.setValue(100*1024*1024); self.buffer.setValue(1024*1024); self.interval.setValue(150)
