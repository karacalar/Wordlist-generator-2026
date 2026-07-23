from dataclasses import dataclass, field, asdict
from pathlib import Path
from .enums import GenerationMode, OutputFormat, Newline
from .character_set import CharacterSetSpec
@dataclass
class OutputSettings:
    directory: Path = Path("output"); base_name:str="combinations"; format:OutputFormat=OutputFormat.TXT; newline:Newline=Newline.CRLF; utf8_bom:bool=False; csv_columns:list[str]=field(default_factory=lambda:["index","generated_value","length","prefix","suffix"]); max_records_per_file:int|None=None; max_bytes_per_file:int|None=None; split_by:str|None=None; buffer_size:int=1024*1024
@dataclass
class FilterSettings:
    must_start_with:str=""; must_end_with:str=""; must_contain:str=""; must_not_contain:str=""; min_digits:int=0; min_letters:int=0; min_uppercase:int=0; min_lowercase:int=0; min_symbols:int=0; disallow_adjacent_repeats:bool=False; max_repeated_char_count:int|None=None; regex:str=""
@dataclass
class GenerationSettings:
    mode:GenerationMode=GenerationMode.FIXED; charset:CharacterSetSpec=field(default_factory=lambda:CharacterSetSpec(["digits"])); exact_length:int=5; min_length:int=1; max_length:int=5; prefixes:list[str]=field(default_factory=lambda:[""]); suffixes:list[str]=field(default_factory=lambda:[""]); position_sets:list[str]=field(default_factory=list); template:str=""; custom_tokens:dict[str,str]=field(default_factory=dict); counter_start:int=0; counter_end:int=99999; counter_step:int=1; counter_padding:int=5; random_count:int=100; secure_random:bool=True; start_index:int=0; end_index:int|None=None; first_n:int|None=None; skip_first:int=0; chunk_number:int|None=None; total_chunks:int|None=None; max_records:int=10_000_000; hard_safety_limit:int=100_000_000; output:OutputSettings=field(default_factory=OutputSettings); filters:FilterSettings=field(default_factory=FilterSettings)
    def to_dict(self):
        d=asdict(self); d["mode"]=str(self.mode); d["output"]["format"]=str(self.output.format); d["output"]["newline"]=str(self.output.newline); d["output"]["directory"]=str(self.output.directory); return d
