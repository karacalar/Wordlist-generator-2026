from enum import StrEnum
class GenerationMode(StrEnum):
    FIXED="fixed"; RANGE="range"; PREFIX_SUFFIX="prefix_suffix"; PATTERN="pattern"; TEMPLATE="template"; COUNTER="counter"; RANDOM_UNIQUE="random_unique"
class OutputFormat(StrEnum):
    TXT="txt"; CSV="csv"; JSONL="jsonl"
class Newline(StrEnum):
    LF="\n"; CRLF="\r\n"
