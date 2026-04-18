from amfi_stream.httpx_client import HttpStreamClient


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def iter_lines(self):
        return ["a", "b", "c"]


class FakeClient:
    def stream(self, *args, **kwargs):
        return FakeResponse()


def test_stream_lines():
    client = HttpStreamClient()
    client._client = FakeClient()

    assert list(client.stream_lines("url")) == ["a", "b", "c"]
