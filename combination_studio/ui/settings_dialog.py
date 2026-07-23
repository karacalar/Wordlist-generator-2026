from PySide6.QtWidgets import QWidget,QFormLayout,QSpinBox
class SettingsPage(QWidget):
    def __init__(self): super().__init__(); f=QFormLayout(self); s=QSpinBox(); s.setMaximum(100000000); s.setValue(10000000); f.addRow('Default max records',s)
