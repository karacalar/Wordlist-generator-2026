import re
from .cartesian_generator import generate_product_from_sets
from ..models.character_set import DIGITS, LOWER, UPPER, dedupe_preserve_order
_PATTERN={"0-9":DIGITS,"A-Z":UPPER,"a-z":LOWER}
def parse_position_pattern(pattern:str)->list[str]:
    sets=[]; pos=0
    for m in re.finditer(r"\[([^\]]+)\]", pattern):
        if m.start()!=pos:
            for ch in pattern[pos:m.start()]: sets.append(ch)
        token=m.group(1); sets.append(_PATTERN.get(token,dedupe_preserve_order(token))); pos=m.end()
    for ch in pattern[pos:]: sets.append(ch)
    return sets
def generate_pattern(pattern_or_sets,start:int=0,end:int|None=None):
    sets=parse_position_pattern(pattern_or_sets) if isinstance(pattern_or_sets,str) else pattern_or_sets
    yield from generate_product_from_sets(sets,start,end)
