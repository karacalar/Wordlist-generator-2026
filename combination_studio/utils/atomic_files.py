from pathlib import Path
import os, tempfile
def atomic_write_text(path, text, encoding='utf-8'):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix=path.name,suffix='.tmp')
    with os.fdopen(fd,'w',encoding=encoding) as f: f.write(text)
    os.replace(tmp,path)
