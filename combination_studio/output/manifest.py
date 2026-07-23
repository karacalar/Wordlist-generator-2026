import json, hashlib
from datetime import datetime, UTC
from pathlib import Path
from .. import __version__
def sha256_file(path):
    h=hashlib.sha256();
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write_manifest(directory:Path,settings,total,index_range,records,status,files):
    data={"application_version":__version__,"generation_mode":str(settings.mode),"character_set_description":settings.charset.describe(),"settings":settings.to_dict(),"total_theoretical_combinations":total,"generated_index_range":index_range,"records_written":records,"completion_time":datetime.now(UTC).isoformat(),"output_files":[{"path":str(Path(f).name),"sha256":sha256_file(f)} for f in files],"status":status}
    p=Path(directory)/"generation_manifest.json"; p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8'); return p
