from datetime import date

from amfi_stream.endpoints import scheme_master_url
from amfi_stream.models import AMFIJob
from amfi_stream.normalisers import normalise_scheme_master
from amfi_stream.sources import StaticURLSource


def stream_scheme_master() -> AMFIJob:
    return AMFIJob(
        name="scheme_master",
        urls_source=StaticURLSource(scheme_master_url()),
        response_delimiter=",",
        response_col_count=10,
        normaliser=normalise_scheme_master,
    )


def stream_latest_nav() -> AMFIJob: ...


def stream_nav_history(from_date: date, to_date: date) -> AMFIJob: ...
