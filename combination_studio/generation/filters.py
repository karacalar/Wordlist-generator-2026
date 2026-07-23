import re
from dataclasses import dataclass
from ..models.generation_settings import FilterSettings
def validate_regex(pattern:str):
    if pattern: re.compile(pattern)
@dataclass
class OutputFilter:
    settings:FilterSettings
    def __post_init__(self): validate_regex(self.settings.regex); self._regex=re.compile(self.settings.regex) if self.settings.regex else None
    def match(self,value:str)->bool:
        s=self.settings
        checks=[not s.must_start_with or value.startswith(s.must_start_with), not s.must_end_with or value.endswith(s.must_end_with), not s.must_contain or s.must_contain in value, not s.must_not_contain or s.must_not_contain not in value]
        if not all(checks): return False
        if sum(c.isdigit() for c in value)<s.min_digits: return False
        if sum(c.isalpha() for c in value)<s.min_letters: return False
        if sum(c.isupper() for c in value)<s.min_uppercase: return False
        if sum(c.islower() for c in value)<s.min_lowercase: return False
        if sum(not c.isalnum() for c in value)<s.min_symbols: return False
        if s.disallow_adjacent_repeats and any(a==b for a,b in zip(value,value[1:])): return False
        if s.max_repeated_char_count is not None and any(value.count(c)>s.max_repeated_char_count for c in set(value)): return False
        return not self._regex or bool(self._regex.search(value))
