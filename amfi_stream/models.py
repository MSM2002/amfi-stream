from collections.abc import Callable
from dataclasses import dataclass

import pyarrow as pa

from amfi_stream.sources import URLSource


@dataclass(frozen=True)
class AMFIJob:
    name: str
    urls_source: URLSource
    response_delimiter: str
    response_col_count: int
    normaliser: Callable[[pa.Table], pa.Table]


@dataclass
class AMFIResult:
    scheme_master: pa.Table | None
    latest_nav: pa.Table | None
    nav_history: pa.Table | None
