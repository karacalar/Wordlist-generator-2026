from shutil import disk_usage
def available_bytes(path): return disk_usage(path).free
def ensure_space(path,required_bytes,safety_margin_bytes=100*1024*1024):
    free=available_bytes(path)
    if required_bytes+safety_margin_bytes>free: raise RuntimeError("estimated output exceeds available disk space plus safety margin")
    return free
