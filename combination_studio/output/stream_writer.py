import csv, json, hashlib
from pathlib import Path
class StreamWriter:
    def __init__(self,path:Path,fmt="txt",newline="\r\n",bom=False,csv_columns=None,buffer_size=1024*1024):
        self.path=Path(path); self.fmt=fmt; self.newline=newline; self.csv_columns=csv_columns or ["index","generated_value","length","prefix","suffix"]; self.records=0; self.bytes_written=0; self.sha256=hashlib.sha256(); self.path.parent.mkdir(parents=True,exist_ok=True)
        enc="utf-8-sig" if bom else "utf-8"; self.file=open(self.path,"w",encoding=enc,newline="",buffering=buffer_size); self.csvw=None
        if fmt=="csv": self.csvw=csv.DictWriter(self.file,fieldnames=self.csv_columns,lineterminator=newline); self.csvw.writeheader()
    def write(self,index:int,value:str,prefix="",suffix=""):
        if self.fmt=="txt": text=value+self.newline
        elif self.fmt=="jsonl": text=json.dumps({"index":index,"value":value},ensure_ascii=False)+self.newline
        else:
            row={"index":index,"generated_value":value,"length":len(value),"prefix":prefix,"suffix":suffix}; before=self.file.tell(); self.csvw.writerow({k:row.get(k,"") for k in self.csv_columns}); self.file.flush(); self.records+=1; self.bytes_written=self.file.tell(); return
        self.file.write(text); data=text.encode('utf-8'); self.sha256.update(data); self.records+=1; self.bytes_written+=len(data)
    def close(self): self.file.flush(); self.file.close()
