from pathlib import Path
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QTextBrowser
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from .. import APP_NAME,__version__,RESPONSIBLE_USE_NOTICE
class AboutPage(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); text=QTextBrowser(); text.setOpenExternalLinks(False); text.setHtml(f"""<h1>{APP_NAME} {__version__}</h1><p>Local-only bounded combination generator for QA and test-data workflows.</p><h2>Responsible use</h2><p>{RESPONSIBLE_USE_NOTICE}</p><ul><li>No network authentication functionality.</li><li>No remote submission.</li><li>No password, hash, or account testing.</li><li>Dependencies: Python, PySide6, pytest, optional psutil, PyInstaller.</li></ul>"""); l.addWidget(text); b=QPushButton('Open local README'); l.addWidget(b); b.clicked.connect(self.open_readme)
    def open_readme(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path('README.md').absolute())))
