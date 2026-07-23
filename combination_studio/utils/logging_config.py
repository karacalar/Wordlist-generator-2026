import logging, sys
from pathlib import Path

def log_dir() -> Path:
    base = Path.home() / "AppData" / "Local" / "Combination Studio" / "logs"
    base.mkdir(parents=True, exist_ok=True)
    return base

def log_file() -> Path:
    return log_dir() / "combination_studio.log"

def configure_logging(level: str = "INFO") -> Path:
    path = log_file()
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(fmt)
    root.addHandler(fh)
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    root.addHandler(sh)
    return path
