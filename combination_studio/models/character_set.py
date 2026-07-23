from dataclasses import dataclass, field
DIGITS="0123456789"; LOWER="abcdefghijklmnopqrstuvwxyz"; UPPER="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SAFE_SYMBOLS="_-+.@#"; TURKISH_LOWER="abcçdefgğhıijklmnoöprsştuüvyz"; TURKISH_UPPER="ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
GROUPS={"digits":DIGITS,"lower":LOWER,"upper":UPPER,"lower_upper":LOWER+UPPER,"letters_digits":LOWER+UPPER+DIGITS,"letters_digits_safe_symbols":LOWER+UPPER+DIGITS+SAFE_SYMBOLS,"hex_lower":"0123456789abcdef","hex_upper":"0123456789ABCDEF","binary":"01","turkish_lower":TURKISH_LOWER,"turkish_upper":TURKISH_UPPER}
def dedupe_preserve_order(text:str)->str:
    seen=set(); out=[]
    for ch in text:
        if ch not in seen: seen.add(ch); out.append(ch)
    return "".join(out)
@dataclass(frozen=True)
class CharacterSetSpec:
    groups:list[str]=field(default_factory=list); custom:str=""; exclude:str=""
    def build(self)->str:
        chars="".join(GROUPS[g] for g in self.groups if g in GROUPS)+self.custom
        chars=dedupe_preserve_order(chars)
        return "".join(ch for ch in chars if ch not in set(self.exclude))
    def describe(self)->dict:
        active=self.build(); return {"groups":self.groups,"custom":self.custom,"exclude":self.exclude,"active":active,"count":len(active)}
