# amfi-stream

Streaming-first ingestion pipeline for AMFI mutual fund data, built on Apache Arrow.

It transforms raw AMFI datasets into schema-safe, analytics-ready tables using a lightweight, parallel streaming engine.

---

## What is amfi-stream

amfi-stream is a data ingestion layer that sits between AMFI data sources and analytics tools.

It is designed for:

- Streaming ingestion of NAV and scheme master data  
- Automatic normalization of AMFI formats  
- Schema enforcement using Apache Arrow  
- Parallel data fetching and processing  
- Clean outputs for downstream analytics systems  

---

## Ecosystem overview

```
AMFI Data Sources (NAV, Scheme Files)
↓
amfi-stream
(Streaming Ingestion Engine)
↓
Sanitization + Normalization
(Arrow Schema Enforcement)
↓
Apache Arrow Tables
↓
Downstream Analytics Tools
(Polars / DuckDB / Pandas / Spark)
```


amfi-stream is a streaming ingestion and normalization layer, not a data API wrapper or analytics engine.

---

## Ecosystem comparison

| Solution | Type | Access Model | Structure | Multi-fund Support | Streaming | Cost | Key Limitation |
|----------|------|--------------|-----------|---------------------|-----------|------|----------------|
| amfi-stream | Ingestion pipeline | Bulk streaming ingestion | Arrow schema enforced | Native dataset-level | Yes | Free | Focused on ingestion, not APIs |
| [mfapi.in](https://www.mfapi.in/) | API service | REST endpoints | JSON structured | Client-side aggregation | Limited | Free | Request-per-fund model |
| [navpipe](https://github.com/MSM2002/navpipe) | SDK | Fund-code queries | Polars output | Requires fund list | Yes | Free | Not dataset ingestion |
| [mftool](https://github.com/NayakwadiS/mftool) | Library | Scraping-based | Partial | Manual aggregation | No | Free | Fragile parsing logic |
| [AMFI India Portal](https://www.amfiindia.com/) | Raw source | File downloads | None | Post-processing required | No | Free | Unstructured format |

---

## Core design principle

- Most tools assume: Data is already structured and ready to consume.
- amfi-stream assumes: Data is streamed, raw, and must be normalized deterministically before analysis.

---

## Features

- Streaming ingestion via HTTP (fsspec)  
- Automatic AMFI data sanitization  
- Schema enforcement using Apache Arrow  
- Parallel execution engine  
- Composable job-based architecture  
- Arrow-native outputs (no Pandas required)  

---

## Quick start

```python
from amfi_stream import AMFIPipeline, stream_latest_nav, stream_scheme_master, stream_historical_nav

jobs = [
    stream_scheme_master(),
    stream_latest_nav(),
    stream_historical_nav("1-May-2025", "1-May-2026")
]

with AMFIPipeline(max_workers=4) as pipeline:
    result = pipeline.run(jobs)

print(result.latest_nav)
```
---

## Output Format

All outputs are returned as PyArrow tables:

```python
AMFIResult(
    scheme_master=pa.Table | None,
    latest_nav=pa.Table | None,
    historical_nav=pa.Table | None,
)
```
---

## Architecture

URL Sources → Streaming Engine → Sanitizer → CSV Parser → Arrow Tables → Normalisers → Pipeline Output

---

## Coming Soon

We are introducing an enhanced output schema that extends raw AMFI NAV data with additional derived, analytics-ready columns.

These improvements will provide a more structured and computation-friendly dataset on top of the standard AMFI format, reducing the need for post-processing in downstream tools and improving compatibility with analytical workflows in Arrow-native environments. 

---

## Design Philosophy

- Streaming over batch processing
- Schema-first ingestion
- Apache Arrow as canonical format
- Minimal dependencies
- Deterministic, reproducible pipelines

---

## Contributing

This project is released under the Apache 2.0 License, and contributions are welcome.

Areas where contributions are especially useful:

- Historical NAV ingestion implementation
- Performance improvements in ingestion engine
- Additional normalization rules for AMFI formats
- Test coverage expansion

---

## License

Apache License 2.0

---
