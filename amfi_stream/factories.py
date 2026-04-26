from datetime import date

from amfi_stream.endpoints import latest_nav_url, scheme_master_url
from amfi_stream.models import AMFIJob
from amfi_stream.normalisers import normalise_latest_nav, normalise_scheme_master
from amfi_stream.sources import StaticURLSource


def stream_scheme_master() -> AMFIJob:
    return AMFIJob(
        name="scheme_master",
        urls_source=StaticURLSource(scheme_master_url()),
        response_delimiter=",",
        response_col_count=10,
        normaliser=normalise_scheme_master,
    )


def stream_latest_nav() -> AMFIJob:
    return AMFIJob(
        name="latest_nav",
        urls_source=StaticURLSource(latest_nav_url()),
        response_delimiter=";",
        response_col_count=6,
        normaliser=normalise_latest_nav,
    )


def stream_nav_histor(from_date: date, to_date: date) -> AMFIJob: ...
