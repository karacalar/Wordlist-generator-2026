import json
from pathlib import Path
from PySide6.QtWidgets import QWidget,QVBoxLayout,QTableWidget,QPushButton,QHBoxLayout,QTableWidgetItem,QMessageBox
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
class HistoryPage(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); self.table=QTableWidget(0,9); self.table.setHorizontalHeaderLabels(['Job name','Mode','Theoretical','Generated','Output size','Status','Start','Completion','Output path']); l.addWidget(self.table)
        row=QHBoxLayout();
        for name in ['Refresh','Open Folder','View Manifest','Reuse Settings','Remove History Entry']:
            b=QPushButton(name); row.addWidget(b); setattr(self,name.lower().split()[0]+'_button',b)
        l.addLayout(row); self.refresh_button.clicked.connect(self.refresh); self.open_button.clicked.connect(self.open_folder); self.view_button.clicked.connect(self.view_manifest); self.remove_button.clicked.connect(self.remove_entry)
    def refresh(self):
        self.table.setRowCount(self.table.rowCount())
    def selected_path(self):
        r=self.table.currentRow(); return self.table.item(r,8).text() if r>=0 and self.table.item(r,8) else ''
    def open_folder(self):
        p=Path(self.selected_path())
        if p.exists(): QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))
        else: QMessageBox.warning(self,'History','Select a valid history output folder.')
    def view_manifest(self):
        p=Path(self.selected_path())/'generation_manifest.json'
        if p.exists(): QMessageBox.information(self,'Manifest',p.read_text(encoding='utf-8')[:5000])
        else: QMessageBox.warning(self,'Manifest','Manifest not found.')
    def remove_entry(self):
        r=self.table.currentRow()
        if r>=0: self.table.removeRow(r)
