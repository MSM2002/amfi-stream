from collections.abc import Iterator

import httpx


class HttpStreamClient:
    def __init__(self, timeout: float = 30.0) -> None:
        self._client = httpx.Client(timeout=timeout)

    def stream_lines(
        self, url: str, params: dict[str, str] | None = None
    ) -> Iterator[str]:
        with self._client.stream("GET", url, params=params) as resp:
            for line in resp.iter_lines():
                yield line
