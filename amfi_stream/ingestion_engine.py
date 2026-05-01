import io
from collections.abc import Iterator

import fsspec
import pyarrow as pa
import pyarrow.csv as pv


class SanitizedStream(io.RawIOBase):
    def __init__(self, generator: Iterator[bytes]):
        self._gen = generator
        self._buffer = b""
        self._closed = False

    def readable(self):
        return True

    def readinto(self, b):
        if self._closed:
            return 0

        target_len = len(b)

        while len(self._buffer) < target_len:
            try:
                self._buffer += next(self._gen)
            except StopIteration:
                self._closed = True
                break

        n = min(len(self._buffer), target_len)
        b[:n] = self._buffer[:n]
        self._buffer = self._buffer[n:]
        return n


class AMFIIngestionEngine:
    def __init__(self) -> None:
        self.fs = fsspec.filesystem("http")

    def _sanitize(
        self, stream, delimiter: bytes, expected_cols: int
    ) -> Iterator[bytes]:
        """
        Stream-safe sanitizer (no seek, no iteration over file object)
        """
        buffer = b""

        while True:
            chunk = stream.read(1 << 16)  # 64KB
            if not chunk:
                break

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

    def _parse(self, stream: Iterator[bytes], delimiter: str) -> pa.Table:
        """
        Fully streaming CSV parse into Arrow
        """
        sanitized_stream = SanitizedStream(stream)

        reader = pv.open_csv(
            sanitized_stream,
            parse_options=pv.ParseOptions(delimiter=delimiter),
            read_options=pv.ReadOptions(block_size=1 << 20),  # 1MB
        )

        batches = []
        for batch in reader:
            batches.append(batch)

        return pa.Table.from_batches(batches)

    def read_one(self, url: str, delimiter: str, col_count: int) -> pa.Table:
        """
        Entry point for one URL
        """
        with self.fs.open(url, "rb", block_size=0) as f:  # streaming mode
            sanitized = self._sanitize(f, delimiter.encode(), col_count)
            table = self._parse(sanitized, delimiter)
            return table
