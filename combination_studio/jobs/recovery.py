import json
from pathlib import Path
from ..utils.atomic_files import atomic_write_text
def save_state(path:Path,settings,last_index:int,active_file:str,records:int,bytes_written:int,status="interrupted"):
    atomic_write_text(path,json.dumps({"settings":settings.to_dict(),"last_completed_global_index":last_index,"active_output_file":active_file,"records_written":records,"byte_count":bytes_written,"job_status":status},indent=2),encoding='utf-8')
def load_state(path:Path): return json.loads(Path(path).read_text(encoding='utf-8'))
def can_resume(path:Path,settings): return Path(path).exists() and load_state(path).get("settings")==settings.to_dict()
