from pathlib import Path
from PySide6.QtWidgets import QWidget,QFormLayout,QHBoxLayout,QLineEdit,QPushButton,QComboBox,QCheckBox,QSpinBox,QFileDialog,QMessageBox
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from ..models.generation_settings import OutputSettings
from ..models.enums import OutputFormat, Newline
class OutputPage(QWidget):
    def __init__(self):
        super().__init__(); f=QFormLayout(self); self.directory=QLineEdit(str(Path('output').absolute())); br=QPushButton('Browse'); op=QPushButton('Open Folder'); row=QHBoxLayout(); row.addWidget(self.directory); row.addWidget(br); row.addWidget(op); f.addRow('Output directory',row)
        self.base=QLineEdit('combinations'); self.format=QComboBox(); self.format.addItems(['TXT','CSV','JSON Lines']); self.bom=QCheckBox('UTF-8 with BOM'); self.newline=QComboBox(); self.newline.addItems(['CRLF','LF']); self.include_index=QCheckBox('Include index in CSV/JSONL'); self.include_index.setChecked(True)
        self.max_records=QSpinBox(); self.max_records.setRange(0,100000000); self.max_bytes=QSpinBox(); self.max_bytes.setRange(0,2_000_000_000); self.manifest=QCheckBox('Generate manifest and SHA-256 checksums'); self.manifest.setChecked(True)
        for label,w in [('Base filename',self.base),('Format',self.format),('Encoding',self.bom),('Newline',self.newline),('Include index',self.include_index),('Split max records (0 disabled)',self.max_records),('Split max bytes (0 disabled)',self.max_bytes),('Manifest',self.manifest)]: f.addRow(label,w)
        br.clicked.connect(self.browse); op.clicked.connect(self.open_folder)
    def browse(self):
        d=QFileDialog.getExistingDirectory(self,'Select output directory',self.directory.text())
        if d: self.directory.setText(d)
    def validate_directory(self):
        p=Path(self.directory.text()).expanduser()
        if not str(p): raise ValueError('Choose an output directory.')
        p.mkdir(parents=True,exist_ok=True); test=p/'.write_test'; test.write_text('ok'); test.unlink(); return p
    def open_folder(self):
        try: p=self.validate_directory(); QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))
        except Exception as e: QMessageBox.warning(self,'Output folder error',str(e))
    def to_settings(self):
        p=self.validate_directory(); fmt={0:OutputFormat.TXT,1:OutputFormat.CSV,2:OutputFormat.JSONL}[self.format.currentIndex()]
        nl=Newline.CRLF if self.newline.currentText()=='CRLF' else Newline.LF
        return OutputSettings(directory=p,base_name=self.base.text() or 'combinations',format=fmt,newline=nl,utf8_bom=self.bom.isChecked(),max_records_per_file=self.max_records.value() or None,max_bytes_per_file=self.max_bytes.value() or None)
