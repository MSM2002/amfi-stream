import httpx


class HttpStreamClient:
    def __init__(self, timeout=30.0):
        self._client = httpx.Client(timeout=timeout)

    def stream_lines(self, url, params=None):
        with self._client.stream("GET", url, params=params) as resp:
            for line in resp.iter_lines():
                yield line
