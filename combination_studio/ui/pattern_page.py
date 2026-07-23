from PySide6.QtWidgets import QWidget,QVBoxLayout,QTableWidget,QTableWidgetItem,QComboBox,QLineEdit,QPushButton,QHBoxLayout
from ..models.character_set import DIGITS,LOWER,UPPER
SETS={'Digit':DIGITS,'Lowercase':LOWER,'Uppercase':UPPER,'Letter':LOWER+UPPER,'Alphanumeric':LOWER+UPPER+DIGITS,'Hexadecimal':'0123456789abcdef','Binary':'01'}
class PatternPage(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); self.table=QTableWidget(0,5); self.table.setHorizontalHeaderLabels(['#','Type','Active characters','Custom/Literal','Delete']); l.addWidget(self.table)
        row=QHBoxLayout(); add=QPushButton('Add position'); preset=QPushButton('Two letters + four digits'); row.addWidget(add); row.addWidget(preset); row.addStretch(); l.addLayout(row); add.clicked.connect(self.add_digit_row); preset.clicked.connect(self.load_default)
        self.load_default()
    def add_digit_row(self): self.add_row('Digit')
    def load_default(self): self.table.setRowCount(0); [self.add_row(t) for t in ['Uppercase','Uppercase','Digit','Digit','Digit','Digit']]
    def add_row(self,t='Digit'):
        r=self.table.rowCount(); self.table.insertRow(r); self.table.setItem(r,0,QTableWidgetItem(str(r+1))); combo=QComboBox(); combo.addItems(list(SETS)+['Custom character set','Fixed literal']); combo.setCurrentText(t); custom=QLineEdit(); preview=QTableWidgetItem(''); delete=QPushButton('Delete')
        self.table.setCellWidget(r,1,combo); self.table.setItem(r,2,preview); self.table.setCellWidget(r,3,custom); self.table.setCellWidget(r,4,delete)
        combo.currentTextChanged.connect(self.refresh); custom.textChanged.connect(self.refresh); delete.clicked.connect(self.remove_selected_row); self.refresh()
    def remove_selected_row(self):
        row=self.table.currentRow()
        if row < 0:
            button=self.sender(); row=self.table.indexAt(button.pos()).row() if button else -1
        if row >= 0: self.table.removeRow(row)
        self.refresh()
    def refresh(self):
        for r in range(self.table.rowCount()):
            self.table.setItem(r,0,QTableWidgetItem(str(r+1))); t=self.table.cellWidget(r,1).currentText(); custom=self.table.cellWidget(r,3).text(); chars=SETS.get(t, custom[:1] if t=='Fixed literal' else custom); self.table.item(r,2).setText(chars)
    def position_sets(self):
        self.refresh(); return [self.table.item(r,2).text() for r in range(self.table.rowCount())]
