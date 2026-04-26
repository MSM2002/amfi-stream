from concurrent.futures import ThreadPoolExecutor

import pyarrow as pa

from amfi_stream.ingestion_engine import AMFIIngestionEngine
from amfi_stream.models import AMFIJob, AMFIResult


class AMFIPipeline:
    def __init__(
        self, executor: ThreadPoolExecutor | None = None, max_workers: int = 8
    ):
        self.engine = AMFIIngestionEngine()
        self.executor = executor or ThreadPoolExecutor(max_workers=max_workers)
        self._owns_executor = executor is None

    def _merge(self, grouped: dict[str, list[pa.Table]], name: str) -> pa.Table | None:
        tables = grouped.get(name)
        if not tables:
            return None
        return pa.concat_tables(tables, promote=True)

    def run(self, jobs: list[AMFIJob]) -> AMFIResult:
        futures = []

        for job in jobs:
            for url in job.urls_source():
                futures.append(
                    (
                        job,
                        self.executor.submit(
                            self.engine.read_one,
                            url,
                            job.response_delimiter,
                            job.response_col_count,
                        ),
                    )
                )

        grouped: dict[str, list[pa.Table]] = {}

        for job, future in futures:
            raw_table = future.result()
            clean_table = job.normaliser(raw_table)

            grouped.setdefault(job.name, []).append(clean_table)

        return AMFIResult(
            scheme_master=self._merge(grouped, "scheme_master"),
            latest_nav=self._merge(grouped, "latest_nav"),
            historical_nav=self._merge(grouped, "historical_nav"),
        )

    def close(self) -> None:
        if self._owns_executor:
            self.executor.shutdown(wait=True)

    def __enter__(self) -> "AMFIPipeline":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
