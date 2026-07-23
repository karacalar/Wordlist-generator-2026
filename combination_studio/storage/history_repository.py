import json
from pathlib import Path
class HistoryRepository:
    def __init__(self,path): self.path=Path(path)
    def load(self): return json.loads(self.path.read_text()) if self.path.exists() else []
    def save(self,records): self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps(records,indent=2),encoding='utf-8')
