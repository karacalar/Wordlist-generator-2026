from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel
class HistoryPage(QWidget):
    def __init__(self): super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel('Local job history: reopen output, inspect manifests, duplicate settings, or remove records without deleting files.'))
