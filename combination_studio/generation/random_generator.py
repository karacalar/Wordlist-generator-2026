import random, secrets
from .index_converter import index_to_combination
def generate_random_unique(charset:str,length:int,count:int,secure:bool=True):
    total=len(charset)**length
    if count>total: raise ValueError("random unique request exceeds theoretical combination space")
    rng=secrets.randbelow if secure else random.randrange; seen=set(); i=0
    while i<count:
        idx=rng(total)
        if idx in seen: continue
        seen.add(idx); yield idx,index_to_combination(idx,charset,length); i+=1
