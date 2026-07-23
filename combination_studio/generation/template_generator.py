import re
from ..models.character_set import DIGITS, LOWER, UPPER
from .cartesian_generator import generate_product_from_sets
TOKENS={"DIGIT":DIGITS,"LOWER":LOWER,"UPPER":UPPER,"LETTER":LOWER+UPPER,"ALNUM":LOWER+UPPER+DIGITS,"HEX":"0123456789abcdef"}
def template_to_position_sets(template:str,custom:dict[str,str]|None=None):
    custom=custom or {}; sets=[]; pos=0
    for m in re.finditer(r"\{([^}]+)\}",template):
        for ch in template[pos:m.start()]: sets.append(ch)
        token=m.group(1)
        if token.startswith("CUSTOM:"): sets.append(custom[token.split(":",1)[1]])
        else: sets.append(TOKENS[token])
        pos=m.end()
    for ch in template[pos:]: sets.append(ch)
    return sets
def generate_template(template,custom=None,start=0,end=None): yield from generate_product_from_sets(template_to_position_sets(template,custom),start,end)
