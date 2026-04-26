from collections.abc import Iterator
from io import BytesIO

import fsspec
import pyarrow as pa
import pyarrow.csv as pv


class AMFIIngestionEngine:
    def __init__(self) -> None:
        self.fs = fsspec.filesystem("http")

    def _sanitize(
        self, stream, delimiter: bytes, expected_cols: int
    ) -> Iterator[bytes]:
        buffer = b""
        for chunk in stream:
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line:
                    continue
                if line.count(delimiter) != expected_cols - 1:
                    continue
                yield line + b"\n"
        # flush remaining buffer
        if buffer and buffer.count(delimiter) == expected_cols - 1:
            yield buffer + b"\n"

    def _parse(self, stream, delimiter) -> pa.Table:
        data = b"".join(stream)
        return pv.read_csv(
            BytesIO(data),
            parse_options=pv.ParseOptions(delimiter=delimiter),
            read_options=pv.ReadOptions(block_size=1 << 22),
        )

    def read_one(self, url: str, delimiter: str, col_count: int) -> pa.Table:
        with self.fs.open(url, "rb") as f:
            sanitized = self._sanitize(f, delimiter.encode(), col_count)
            table = self._parse(sanitized, delimiter)
            return table
