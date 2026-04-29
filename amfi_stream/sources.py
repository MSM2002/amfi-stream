from datetime import date, timedelta
from typing import Protocol

from amfi_stream.endpoints import historical_nav_url


class URLSource(Protocol):
    def __call__(self) -> list[str]: ...


class StaticURLSource:
    def __init__(self, url: str) -> None:
        self.url = url

    def __call__(self) -> list[str]:
        return [self.url]


class HistoricalNAVSource:
    MAX_DAY_RANGE_FOR_HISTORICAL_NAV_RESPONSE = 90

    def __init__(self, from_date: date, to_date: date):
        self.from_date = from_date
        self.to_date = to_date

    def __call__(self) -> list[str]:
        urls = []
        for f, t in self._date_chunker():
            urls.append(historical_nav_url(f, t))
        return urls

    def _date_chunker(self) -> list[tuple[date, date]]:
        date_chunks = []
        current_start_date = self.from_date
        end_date = self.to_date
        while current_start_date <= end_date:
            current_end_date = current_start_date + timedelta(
                days=self.MAX_DAY_RANGE_FOR_HISTORICAL_NAV_RESPONSE - 1
            )
            actual_end_date = min(current_end_date, end_date)
            date_chunks.append((current_start_date, actual_end_date))
            current_start_date = actual_end_date + timedelta(days=1)
        return date_chunks
