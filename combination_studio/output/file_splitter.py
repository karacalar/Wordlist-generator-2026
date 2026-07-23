from pathlib import Path
from .stream_writer import StreamWriter
class FileSplitter:
    def __init__(self,directory:Path,base_name="combinations",fmt="txt",max_records=None,max_bytes=None,**writer_kw):
        self.dir=Path(directory); self.base=base_name; self.fmt=fmt; self.max_records=max_records; self.max_bytes=max_bytes; self.kw=writer_kw; self.files=[]; self.current=None; self.no=0
    def _open(self):
        self.no+=1; p=self.dir/f"{self.base}_{self.no:04d}.{self.fmt}"; self.current=StreamWriter(p,self.fmt,**self.kw); self.files.append(self.current)
    def write(self,index,value,prefix="",suffix=""):
        if self.current is None or (self.max_records and self.current.records>=self.max_records) or (self.max_bytes and self.current.bytes_written>=self.max_bytes): self._open()
        self.current.write(index,value,prefix,suffix)
    def close(self):
        if self.current: self.current.close()
