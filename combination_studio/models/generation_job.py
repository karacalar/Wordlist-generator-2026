from dataclasses import dataclass, field
from datetime import datetime, UTC
from .generation_settings import GenerationSettings
@dataclass
class GenerationJob:
    settings:GenerationSettings; job_name:str="Generation Job"; status:str="pending"; started_at:str=field(default_factory=lambda:datetime.now(UTC).isoformat()); completed_at:str|None=None; records_written:int=0; bytes_written:int=0; last_index:int=-1
