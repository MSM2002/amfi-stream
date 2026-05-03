import pyarrow as pa
from typing import Literal
import re

CASE_STYLE = Literal["lower", "upper", "title", "snake", "camel", "pascal", "kebab"]

_WORD_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)|\d+")


def convert_column_case(table: pa.Table, case: CASE_STYLE) -> pa.Table:
    return table.rename_columns([
        _transform_column_name(name, case)
        for name in table.column_names
    ])


def _transform_column_name(name: str, case: CASE_STYLE) -> str:
    words = [w.lower() for w in _WORD_RE.findall(name)]

    if not words:
        return name 

    capitalized = [w.capitalize() for w in words]

    transformers = {
        "lower": lambda: " ".join(words),
        "upper": lambda: " ".join(w.upper() for w in words),
        "title": lambda: " ".join(capitalized),
        "snake": lambda: "_".join(words),
        "camel": lambda: words[0] + "".join(capitalized[1:]),
        "pascal": lambda: "".join(capitalized),
        "kebab": lambda: "-".join(words),
    }

    try:
        return transformers[case]()
    except KeyError:
        raise ValueError(f"Unsupported case style: {case}")