"""Engineering FEA result analytics. This analyzes exported result tables; it is not an FEA solver."""
from __future__ import annotations
import pandas as pd

REQUIRED = {"node_id", "x", "y", "z", "displacement", "von_mises"}

def analyze_fea(rows: list[dict], yield_strength_mpa: float | None = None) -> dict:
    if not rows:
        raise ValueError("At least one node result row is required")
    frame = pd.DataFrame(rows)
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError("Missing FEA columns: " + ", ".join(sorted(missing)))
    numeric = ["x", "y", "z", "displacement", "von_mises"]
    for col in numeric:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna(subset=numeric)
    if frame.empty:
        raise ValueError("No valid numeric FEA rows")
    max_stress = float(frame["von_mises"].max())
    max_disp = float(frame["displacement"].abs().max())
    result = {
        "node_count": int(len(frame)),
        "max_von_mises_mpa": max_stress,
        "mean_von_mises_mpa": float(frame["von_mises"].mean()),
        "max_displacement": max_disp,
        "mean_displacement": float(frame["displacement"].abs().mean()),
        "critical_node_id": str(frame.loc[frame["von_mises"].idxmax(), "node_id"]),
        "mesh": {
            "x": frame["x"].astype(float).tolist(),
            "y": frame["y"].astype(float).tolist(),
            "z": frame["z"].astype(float).tolist(),
            "stress": frame["von_mises"].astype(float).tolist()
        },
        "note": "Post-processing of supplied nodal results only; no mesh solver is run."
    }
    if yield_strength_mpa is not None:
        if yield_strength_mpa <= 0:
            raise ValueError("yield_strength_mpa must be positive")
        result["factor_of_safety"] = float(yield_strength_mpa / max_stress) if max_stress > 0 else None
        result["yield_strength_mpa"] = float(yield_strength_mpa)
    return result
