from __future__ import annotations
import numpy as np
import pandas as pd


def analyze_velocity_field(rows: list[dict]):
    required = {"x", "y", "u", "v"}
    frame = pd.DataFrame(rows)
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required CFD columns: {', '.join(sorted(missing))}")
    for col in required:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame = frame.dropna(subset=list(required))
    if frame.empty:
        raise ValueError("No valid velocity samples")
    speed = np.hypot(frame.u.to_numpy(), frame.v.to_numpy())
    frame["velocity_magnitude"] = speed
    return {"sample_count":int(len(frame)), "mean_speed":float(np.mean(speed)), "max_speed":float(np.max(speed)),
            "min_speed":float(np.min(speed)), "rms_speed":float(np.sqrt(np.mean(speed**2))),
            "vectors":frame[["x","y","u","v","velocity_magnitude"]].to_dict(orient="records"),
            "scope":"CFD exported-field post-processing only; does not solve Navier-Stokes equations"}
