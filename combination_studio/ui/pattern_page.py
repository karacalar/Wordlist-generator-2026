from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit
class PatternPage(QWidget):
    def __init__(self): super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel('Visual position editor: use [A-Z][A-Z][0-9][0-9] or literal fixed characters.')); l.addWidget(QLineEdit('[A-Z][A-Z][0-9][0-9][0-9][0-9]'))
