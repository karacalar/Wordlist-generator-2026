from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QGroupBox,QTextEdit,QPushButton,QCheckBox,QLabel,QFileDialog,QMessageBox

def normalize_lines(text, trim=True, preserve_empty=True, dedupe=True):
    raw=text.splitlines(); out=[]; dup=0; seen=set()
    for line in raw:
        v=line.strip() if trim else line
        if v=="" and not preserve_empty: continue
        if dedupe and v in seen: dup+=1; continue
        seen.add(v); out.append(v)
    return out or [""], dup
class _Panel(QGroupBox):
    def __init__(self,title):
        super().__init__(title); l=QVBoxLayout(self); self.editor=QTextEdit(); self.editor.setPlaceholderText('One value per line. Blank means no '+title.lower()[:-1]+'.'); l.addWidget(self.editor)
        row=QHBoxLayout(); self.load=QPushButton('Load TXT'); self.clear=QPushButton('Clear'); row.addWidget(self.load); row.addWidget(self.clear); l.addLayout(row)
        self.trim=QCheckBox('Trim whitespace'); self.trim.setChecked(True); self.empty=QCheckBox('Preserve intentional empty value'); self.empty.setChecked(True); self.dedupe=QCheckBox('Remove duplicates'); self.dedupe.setChecked(True)
        for w in (self.trim,self.empty,self.dedupe): l.addWidget(w)
        self.count=QLabel('Count: 1, duplicates removed: 0'); l.addWidget(self.count)
        self.clear.clicked.connect(self.editor.clear); self.load.clicked.connect(self.load_file)
        for w in (self.editor,self.trim,self.empty,self.dedupe):
            sig=getattr(w,'textChanged',None) or getattr(w,'stateChanged',None); sig.connect(self.update_count)
    def values(self): return normalize_lines(self.editor.toPlainText(),self.trim.isChecked(),self.empty.isChecked(),self.dedupe.isChecked())
    def update_count(self):
        vals, dup=self.values(); self.count.setText(f'Count: {len(vals)}, duplicates removed: {dup}')
    def load_file(self):
        path,_=QFileDialog.getOpenFileName(self,'Load TXT','','Text files (*.txt);;All files (*)')
        if not path: return
        try: self.editor.setPlainText(open(path,encoding='utf-8').read())
        except OSError as e: QMessageBox.warning(self,'Could not load file',str(e))
class PrefixSuffixPage(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); row=QHBoxLayout(); self.prefixes=_Panel('Prefixes'); self.suffixes=_Panel('Suffixes'); row.addWidget(self.prefixes); row.addWidget(self.suffixes); l.addLayout(row); self.preview=QLabel(); self.preview.setWordWrap(True); l.addWidget(self.preview)
        self.prefixes.editor.textChanged.connect(self.update_preview); self.suffixes.editor.textChanged.connect(self.update_preview); self.update_preview()
    def update_preview(self): self.preview.setText(f'Normalized preview: prefixes={self.get_prefixes()[:5]}, suffixes={self.get_suffixes()[:5]}')
    def get_prefixes(self): return self.prefixes.values()[0]
    def get_suffixes(self): return self.suffixes.values()[0]
