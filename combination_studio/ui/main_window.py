from PySide6.QtWidgets import QMainWindow,QTabWidget,QLabel,QWidget,QVBoxLayout
from .generator_page import GeneratorPage
from .pattern_page import PatternPage
from .filters_page import FiltersPage
from .output_page import OutputPage
from .history_page import HistoryPage
from .settings_dialog import SettingsPage
from .. import RESPONSIBLE_USE_NOTICE
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Combination Studio'); self.resize(1100,750); tabs=QTabWidget(); self.setCentralWidget(tabs)
        tabs.addTab(GeneratorPage(),"Generator"); tabs.addTab(PatternPage(),"Position Pattern"); tabs.addTab(simple('Load, trim, preserve, and deduplicate prefix/suffix lists.'),"Prefixes and Suffixes"); tabs.addTab(FiltersPage(),"Filters"); tabs.addTab(OutputPage(),"Output"); tabs.addTab(HistoryPage(),"Job History"); tabs.addTab(SettingsPage(),"Settings"); tabs.addTab(simple(RESPONSIBLE_USE_NOTICE),"About and Responsible Use")
def simple(text):
    w=QWidget(); l=QVBoxLayout(w); lab=QLabel(text); lab.setWordWrap(True); l.addWidget(lab); return w
