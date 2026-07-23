def index_to_combination(index:int, charset:str, length:int)->str:
    if not charset: raise ValueError("character set cannot be empty")
    if index < 0: raise ValueError("index cannot be negative")
    base=len(charset); total=base**length
    if index>=total: raise IndexError("index outside combination space")
    chars=[charset[0]]*length
    for pos in range(length-1,-1,-1):
        index, rem = divmod(index, base); chars[pos]=charset[rem]
    return "".join(chars)
def combination_to_index(value:str, charset:str)->int:
    base=len(charset); lookup={c:i for i,c in enumerate(charset)}; n=0
    for ch in value: n=n*base+lookup[ch]
    return n
def normalize_range(total:int,start:int=0,end:int|None=None,first_n:int|None=None,skip_first:int=0,chunk_number:int|None=None,total_chunks:int|None=None)->tuple[int,int]:
    s=max(0,start+skip_first); e=total-1 if end is None else min(end,total-1)
    if first_n is not None: e=min(e,s+first_n-1)
    if chunk_number and total_chunks:
        size=(total+total_chunks-1)//total_chunks; s=max(s,(chunk_number-1)*size); e=min(e,chunk_number*size-1,total-1)
    if e<s: return (0,-1)
    return s,e
