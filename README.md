# ⚡ amfi-stream

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Arrow](https://img.shields.io/badge/Apache-Arrow-orange)
![Status](https://img.shields.io/badge/status-active-success)
![Built For](https://img.shields.io/badge/built%20for-data%20pipelines-black)

**Streaming-first ingestion for AMFI mutual fund data.**

Turn raw AMFI files into **clean, schema-safe, analytics-ready Arrow tables** — in parallel, without hacks.

---

## 🚀 The problem (you already know this)

AMFI data is:

- inconsistent  
- semi-structured  
- painful to clean  
- not pipeline-friendly  

Every existing tool assumes:

> “just fetch and parse it”

That breaks at scale.

---

## ⚡ The shift

> **Don’t query AMFI. Ingest it properly.**

---

## 🧩 What amfi-stream does

```
Raw AMFI Data
(NAV + Scheme Files)
        ↓
⚡ amfi-stream
(stream + sanitize + normalize)
        ↓
Arrow Tables (typed, clean)
        ↓
Polars / DuckDB / Pandas / Spark
```

---

## ✨ Why people switch

- ⚡ Streaming instead of batch downloads  
- 🧼 Automatic normalization (no manual cleaning)  
- 🧱 Strong schema via Apache Arrow  
- 🧵 Parallel ingestion engine  
- 📊 Directly usable in analytics tools  
- 🐼 No Pandas dependency  

---

## 🆚 Alternatives (quick reality check)

| Tool | Model | Why it breaks |
|------|------|---------------|
| mfapi.in | API calls | One request per fund → slow |
| navpipe | SDK | Needs pre-known fund list |
| mftool | Scraper | Fragile, breaks silently |
| AMFI site | Raw files | No structure |

**amfi-stream:**

✔ Dataset-level ingestion  
✔ Streaming + parallel  
✔ Schema enforced  
✔ Built for pipelines  

---

## ⚡ Quick start

```python
from amfi_stream import (
    AMFIPipeline,
    stream_latest_nav,
    stream_scheme_master,
    stream_historical_nav
)

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

## 📦 Output

```python
AMFIResult(
    scheme_master=pa.Table | None,
    latest_nav=pa.Table | None,
    historical_nav=pa.Table | None,
)
```

**Typed. Predictable. Analytics-ready.**

---

## 🏗 Architecture

```
URLs
 ↓
Streaming Engine
 ↓
Sanitizer
 ↓
Parser
 ↓
Arrow Tables
 ↓
Normalizers
 ↓
Pipeline Output
```

---

## 🔥 Design principles

- Streaming > batch  
- Schema > guesswork  
- Arrow > DataFrame conversions  
- Deterministic > fragile parsing  
- Minimal > bloated  

---

## 🔮 Coming soon

- Derived analytics-ready columns  
- Enhanced schema layers  
- Faster historical ingestion  

---

## 🤝 Contributing

If you’ve ever fought AMFI data, you already know why this exists.

Open areas:
- Performance tuning
- Enhanced schema creation
- Benchmark comparison
- Tests
- Documentation and docstrings

---

## ⭐ If this helped you

Give it a star — it helps more people discover a better way to handle AMFI data.

---

## 📜 License

Apache 2.0