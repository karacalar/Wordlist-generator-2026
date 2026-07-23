def grouped(n:int)->str: return f"{n:,}"
def grouped_scientific(n:int)->str: return f"{n:,} ({n:.14e})"
def bytes_human(n:int)->str:
    for u in ['B','KB','MB','GB','TB','PB']:
        if n<1024: return f"{n:.1f} {u}"
        n/=1024
    return f"{n:.1f} EB"
