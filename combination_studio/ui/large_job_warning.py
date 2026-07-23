from PySide6.QtWidgets import QMessageBox
class LargeJobWarning(QMessageBox):
    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Large Job Warning')
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
