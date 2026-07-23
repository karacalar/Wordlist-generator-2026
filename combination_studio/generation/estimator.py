from dataclasses import dataclass
from math import prod
from shutil import disk_usage
from pathlib import Path
from .counter_generator import counter_count
@dataclass
class Estimate:
    total:int; bytes_per_line:int; estimated_bytes:int; approx_files:int; available_bytes:int; feasible:bool; warning:str=""
def sci(n:int)->str: return f"{n:,}\n{n:.14e}"
def estimate_uniform(charset_size:int,length:int,prefixes=None,suffixes=None,newline="\r\n",fmt="txt",available_path=".",max_records_per_file=None)->Estimate:
    if charset_size<=0: raise ValueError("empty character set")
    prefixes=prefixes or [""]; suffixes=suffixes or [""]; total=(charset_size**length)*len(prefixes)*len(suffixes)
    sample=max(len((p+('x'*length)+s).encode('utf-8')) for p in prefixes for s in suffixes)+len(newline.encode())
    if fmt=="csv": sample+=20
    if fmt=="jsonl": sample+=25
    est=total*sample; from pathlib import Path
    ap=Path(available_path); probe=ap if ap.exists() else ap.parent
    avail=disk_usage(probe).free; files=(total+(max_records_per_file or total)-1)//(max_records_per_file or total) if total else 0
    return Estimate(total,sample,est,files,avail,est<avail, "Estimated output exceeds available disk space" if est>=avail else "")
def estimate_range(charset_size:int,min_length:int,max_length:int,**kw)->Estimate:
    e=estimate_uniform(charset_size,1,**kw); total=sum(charset_size**n for n in range(min_length,max_length+1)); e.total=total; e.estimated_bytes=total*e.bytes_per_line; e.feasible=e.estimated_bytes<e.available_bytes; return e
def estimate_positions(position_sets:list[str],prefixes=None,suffixes=None,newline="\r\n",available_path=".")->Estimate:
    if any(not s for s in position_sets): raise ValueError("empty position character set")
    length=len(position_sets); total=prod(len(s) for s in position_sets)*len(prefixes or [""])*len(suffixes or [""])
    return estimate_uniform(1,length,prefixes,suffixes,newline,available_path=available_path).__class__(total, length+len(newline), total*(length+len(newline)),1,disk_usage(Path(available_path) if Path(available_path).exists() else Path(available_path).parent).free,total*(length+len(newline))<disk_usage(Path(available_path) if Path(available_path).exists() else Path(available_path).parent).free,"")
