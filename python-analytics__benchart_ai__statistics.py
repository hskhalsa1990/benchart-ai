from __future__ import annotations
import pandas as pd


def summarize(frame: pd.DataFrame) -> dict:
    """Return count, mean, median, spread and percentile metrics per benchmark."""
    if frame.empty:
        return {"benchmarks": [], "rows": 0}
    grouped = frame.groupby(["group", "name", "unit"], dropna=False)["value"]
    rows = []
    for (group, name, unit), values in grouped:
        rows.append({
            "group": str(group), "name": str(name), "unit": str(unit),
            "count": int(values.count()), "mean": float(values.mean()),
            "median": float(values.median()), "std": float(values.std(ddof=1)) if values.count() > 1 else 0.0,
            "min": float(values.min()), "max": float(values.max()),
            "p90": float(values.quantile(.90)), "p95": float(values.quantile(.95)),
            "p99": float(values.quantile(.99)),
        })
    return {"rows": int(len(frame)), "benchmarks": rows}


def compare_groups(frame: pd.DataFrame, baseline: str, candidate: str) -> list[dict]:
    """Compare group means; positive delta means candidate is higher/slower."""
    means = frame.groupby(["name", "unit", "group"])["value"].mean().unstack("group")
    if baseline not in means.columns or candidate not in means.columns:
        raise ValueError("Baseline or candidate group was not found")
    result = []
    for (name, unit), row in means.iterrows():
        before, after = row.get(baseline), row.get(candidate)
        if pd.isna(before) or pd.isna(after):
            continue
        delta = float(after - before)
        pct = (delta / float(before) * 100.0) if float(before) != 0 else None
        result.append({"name": str(name), "unit": str(unit), "baseline": float(before),
                       "candidate": float(after), "delta": delta, "change_percent": pct,
                       "status": "better" if delta < 0 else "worse" if delta > 0 else "unchanged"})
    return result
