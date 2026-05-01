from datetime import date, datetime


class DateParser:
    FORMATS = (
        "%Y-%m-%d",  # ISO
        "%d-%b-%Y",  # AMFI
    )

    @classmethod
    def parse(cls, value: str | date) -> date:
        if isinstance(value, date):
            return value

        if not isinstance(value, str):
            raise TypeError(f"Expected str or date, got {type(value).__name__}")

        parsed = cls._parse_str(value)
        if parsed is not None:
            return parsed

        raise ValueError(
            f"Invalid date format: {value}. Supported formats: {cls.FORMATS}"
        )

    @classmethod
    def _parse_str(cls, value: str) -> date | None:
        for fmt in cls.FORMATS:
            result = cls._try_format(value, fmt)
            if result is not None:
                return result
        return None

    @staticmethod
    def _try_format(value: str, fmt: str) -> date | None:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            return None
