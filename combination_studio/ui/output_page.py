from PySide6.QtWidgets import QWidget,QFormLayout,QComboBox,QSpinBox,QLineEdit
class OutputPage(QWidget):
    def __init__(self): super().__init__(); f=QFormLayout(self); c=QComboBox(); c.addItems(['TXT','CSV','JSON Lines']); f.addRow('Output format',c); f.addRow('Output folder',QLineEdit('output')); f.addRow('Max records per file',QSpinBox()); f.addRow('Max file size bytes',QSpinBox())
