from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {"name", "value"}


def load_benchmark_csv(path: str) -> pd.DataFrame:
    """Load a CSV containing at least name and value columns."""
    frame = pd.read_csv(path)
    return clean_benchmark_frame(frame)


def clean_benchmark_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize benchmark rows without silently inventing missing measurements.

    Accepted columns: name, value, unit (optional), group (optional), run (optional).
    Invalid/non-numeric values are removed and reported by the caller via row counts.
    """
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    result = frame.copy()
    result["name"] = result["name"].astype("string").str.strip()
    result["value"] = pd.to_numeric(result["value"], errors="coerce")
    result = result.dropna(subset=["name", "value"])
    result = result[result["name"].ne("")]
    if "unit" not in result:
        result["unit"] = ""
    if "group" not in result:
        result["group"] = "default"
    if "run" not in result:
        result["run"] = 1
    result["group"] = result["group"].fillna("default").astype(str)
    result["unit"] = result["unit"].fillna("").astype(str)
    return result.reset_index(drop=True)
