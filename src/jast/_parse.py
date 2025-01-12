import enum

from jast._jast import JAST


class ParseMode(enum.Enum):
    UNIT = "unit"
    METH = "meth"
    STMT = "stmt"
    EXPR = "expr"

def parse(src: str, mode: ParseMode | str | int = ParseMode.UNIT) -> JAST:
    if isinstance(mode, str):
        mode = ParseMode[mode]
    elif isinstance(mode, int):
        mode = list(ParseMode)[mode]
