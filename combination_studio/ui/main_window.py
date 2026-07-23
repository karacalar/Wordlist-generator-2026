from PySide6.QtWidgets import QMainWindow,QTabWidget,QMessageBox,QPlainTextEdit,QDockWidget
from PySide6.QtCore import Qt
from .generator_page import GeneratorPage
from .pattern_page import PatternPage
from .prefix_suffix_page import PrefixSuffixPage
from .filters_page import FiltersPage
from .output_page import OutputPage
from .history_page import HistoryPage
from .settings_dialog import SettingsPage
from .about_page import AboutPage
from ..utils.logging_config import log_file
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Combination Studio'); self.resize(1200,820); tabs=QTabWidget(); self.setCentralWidget(tabs)
        self.pattern=PatternPage(); self.prefix_suffix=PrefixSuffixPage(); self.filters=FiltersPage(); self.output=OutputPage(); self.history=HistoryPage(); self.settings=SettingsPage(); self.generator=GeneratorPage(self.pattern,self.prefix_suffix,self.filters,self.output,self.settings)
        tabs.addTab(self.generator,'Generator'); tabs.addTab(self.pattern,'Position Pattern'); tabs.addTab(self.prefix_suffix,'Prefixes and Suffixes'); tabs.addTab(self.filters,'Filters'); tabs.addTab(self.output,'Output'); tabs.addTab(self.history,'Job History'); tabs.addTab(self.settings,'Settings'); tabs.addTab(AboutPage(),'About and Responsible Use')
        self.log_panel=QPlainTextEdit(); self.log_panel.setReadOnly(True); dock=QDockWidget('Application Log',self); dock.setWidget(self.log_panel); self.addDockWidget(Qt.BottomDockWidgetArea,dock); self.refresh_log()
    def refresh_log(self):
        p=log_file(); self.log_panel.setPlainText(p.read_text(encoding='utf-8')[-8000:] if p.exists() else 'Log will appear here after application activity.')
    def closeEvent(self,event):
        if getattr(self.generator,'thread',None):
            if QMessageBox.question(self,'Generation running','A generation job is active. Stop it and close?') != QMessageBox.Yes: event.ignore(); return
            self.generator.stop_generation()
        event.accept()
