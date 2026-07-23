from PySide6.QtWidgets import QWidget,QFormLayout,QLineEdit,QCheckBox,QSpinBox,QLabel
class FiltersPage(QWidget):
    def __init__(self): super().__init__(); f=QFormLayout(self); f.addRow(QLabel('Filters are local and may require evaluating many candidates.')); [f.addRow(x,QLineEdit()) for x in ['Must start with','Must end with','Must contain','Must not contain','Regular expression']]; f.addRow('Disallow adjacent repeats',QCheckBox()); f.addRow('Minimum digit count',QSpinBox())
