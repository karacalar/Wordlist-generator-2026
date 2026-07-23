def generate_counter(start:int,end:int,step:int=1,padding:int=0,prefix:str="",suffix:str=""):
    if step==0: raise ValueError("step cannot be zero")
    i=0
    for n in range(start,end + (1 if step>0 else -1), step):
        yield i, f"{prefix}{n:0{padding}d}{suffix}"; i+=1
def counter_count(start:int,end:int,step:int=1)->int:
    if step==0: raise ValueError("step cannot be zero")
    if (step>0 and start>end) or (step<0 and start<end): return 0
    return abs((end-start)//step)+1
