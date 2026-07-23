from itertools import product
from .index_converter import index_to_combination, normalize_range
def generate_fixed(charset:str,length:int,start:int=0,end:int|None=None):
    total=len(charset)**length; s,e=normalize_range(total,start,end)
    for i in range(s,e+1): yield i,index_to_combination(i,charset,length)
def generate_range(charset:str,min_length:int,max_length:int,start:int=0,end:int|None=None):
    offset=0
    for length in range(min_length,max_length+1):
        total=len(charset)**length; s=max(0,start-offset); e=total-1 if end is None else min(total-1,end-offset)
        if e>=s:
            for local in range(s,e+1): yield offset+local,index_to_combination(local,charset,length)
        offset += total
        if end is not None and offset>end: break
def generate_product_from_sets(position_sets:list[str],start:int=0,end:int|None=None):
    total=1
    for s in position_sets:
        if not s: raise ValueError("position character set cannot be empty")
        total*=len(s)
    from .index_converter import normalize_range
    s,e=normalize_range(total,start,end)
    for idx in range(s,e+1):
        n=idx; out=[]
        for chars in reversed(position_sets):
            n, rem=divmod(n,len(chars)); out.append(chars[rem])
        yield idx,"".join(reversed(out))
