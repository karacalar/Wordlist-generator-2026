import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from . import APP_NAME, RESPONSIBLE_USE_NOTICE
from .ui.main_window import MainWindow
def main():
    app=QApplication(sys.argv); app.setApplicationName(APP_NAME)
    QMessageBox.information(None,"Responsible Use",RESPONSIBLE_USE_NOTICE)
    w=MainWindow(); w.show(); return app.exec()
