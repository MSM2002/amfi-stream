class StreamFilter:
    def apply(self, line: str) -> str | None:
        line = line.strip()
        if not line:
            return None
        return line
