# Benchart AI – Python Analytics Companion

This is an **optional companion service** for the original Benchart Kotlin/Compose application. It does not replace or modify the existing benchmark parser or UI. It accepts normalized CSV/JSON benchmark rows and adds Python data-science workflows.

## Included modules

- **Pandas + NumPy ecosystem:** CSV ingestion, numeric coercion, missing/invalid row cleanup, grouped analysis.
- **Statistics:** count, mean, median, sample standard deviation, min/max, P90/P95/P99.
- **Benchmark comparison:** baseline vs candidate deltas, percentage change and better/worse status (lower values are treated as better, matching latency-style benchmarks).
- **Machine learning:** Isolation Forest anomaly detection and a Random Forest run-trend estimate. Predictions are experimental, not guarantees.
- **Visualization:** grouped PNG chart export through Matplotlib.
- **Computer vision benchmark:** optional OpenCV image-resize timing and throughput test.
- **REST API:** FastAPI endpoints for health, analysis, comparisons and anomaly detection.
- **CLI + tests:** local CSV workflow and unit tests.

Deep learning is deliberately an **optional extension point**, not falsely represented as a trained model. Install PyTorch from the official selector appropriate to your CPU/GPU before building neural-network workflows. The core service does not require a GPU.

## CSV format

Required columns: `name,value`. Optional columns: `unit,group,run`.

```csv
name,value,unit,group,run
startup,120,ms,before,1
startup,110,ms,after,1
```

## Install (desktop / Linux / Termux)

```bash
cd python-analytics
python -m venv .venv
# Linux / Termux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Optional computer vision / deep learning packages are large; install only when required:

```bash
pip install -r requirements-optional.txt
```

On Android/Termux, PyTorch and OpenCV wheels may not be available for every device/Python version. Run the core analytics first; use a compatible Linux/desktop environment for optional heavy packages.

## CLI

```bash
benchart-ai examples/sample_benchmarks.csv --anomalies --chart report.png
```

Or without installing the console script:

```bash
PYTHONPATH=. python -m benchart_ai.cli examples/sample_benchmarks.csv --anomalies --chart report.png
```

## REST API

```bash
uvicorn benchart_ai.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

Example request to `/compare`:

```json
{
  "baseline": "before",
  "candidate": "after",
  "rows": [
    {"name": "startup", "value": 120, "unit": "ms", "group": "before", "run": 1},
    {"name": "startup", "value": 110, "unit": "ms", "group": "after", "run": 1}
  ]
}
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Architecture / next integration step

`python-analytics/` is intentionally isolated from the Kotlin Multiplatform source tree. A later UI integration can send parsed benchmark rows to this service using HTTP, while the original Benchart web build remains usable without Python. Do not expose the API publicly without authentication, request limits and deployment hardening.


## Jupyter Notebook Lab

Install notebook dependencies with `pip install -r requirements-notebook.txt`, then run `jupyter lab` and open `notebooks/Benchart_AI_Engineering_DataScience_Lab.ipynb`. It contains runnable examples for benchmark analytics, Pandas cleaning, ML, beam SFD/BMD, interactive Plotly 3D graphs, CFD/FEA exported-result visualization, engineering calculators, DOE, and timetable charts. Generated files are saved to `outputs/`.
