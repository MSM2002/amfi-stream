from datetime import date
from typing import Protocol

from amfi_stream.endpoints import nav_history_url


class URLSource(Protocol):
    def __call__(self) -> list[str]: ...


class StaticURLSource:
    def __init__(self, url: str):
        self.url = url

    def __call__(self) -> list[str]:
        return [self.url]


class NavHistorySource:
    def __init__(self, from_date: date, to_date: date):
        self.from_date = from_date
        self.to_date = to_date

    def __call__(self) -> list[str]:
        urls = []
        for f, t in self.chunker():
            urls.append(nav_history_url(f, t))
        return urls

    def chunker(self): ...
