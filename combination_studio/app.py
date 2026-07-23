import sys, logging, traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from . import APP_NAME, RESPONSIBLE_USE_NOTICE
from .ui.main_window import MainWindow
from .utils.logging_config import configure_logging

def excepthook(exc_type, exc, tb):
    logging.getLogger(__name__).error('Unhandled GUI exception', exc_info=(exc_type, exc, tb))
    QMessageBox.critical(None,'Unhandled error', ''.join(traceback.format_exception_only(exc_type, exc)))

def main():
    configure_logging(); sys.excepthook=excepthook
    app=QApplication(sys.argv); app.setApplicationName(APP_NAME)
    QMessageBox.information(None,'Responsible Use',RESPONSIBLE_USE_NOTICE)
    w=MainWindow(); w.show(); return app.exec()
