from amfi_stream.factories import (
    stream_historical_nav,
    stream_latest_nav,
    stream_scheme_master,
)
from amfi_stream.pipeline import AMFIPipeline

__all__ = [
    "AMFIPipeline",
    "stream_latest_nav",
    "stream_scheme_master",
    "stream_historical_nav",
]

__version__ = "0.2.0"
