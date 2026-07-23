from dataclasses import dataclass
@dataclass
class HistoryRecord: job_name:str; mode:str; settings_summary:str; theoretical_count:int; generated_count:int; output_size:int; status:str; start_time:str; completion_time:str; output_directory:str
