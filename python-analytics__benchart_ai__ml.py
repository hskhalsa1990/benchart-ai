from __future__ import annotations
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


def detect_anomalies(frame: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """Flag unusual values within each benchmark using Isolation Forest."""
    if not 0 < contamination < 0.5:
        raise ValueError("contamination must be between 0 and 0.5")
    pieces = []
    for _, group in frame.groupby(["group", "name", "unit"], dropna=False):
        part = group.copy()
        if len(part) < 5 or part["value"].nunique() < 2:
            part["anomaly"] = False
            part["anomaly_score"] = 0.0
        else:
            model = IsolationForest(contamination=contamination, random_state=42)
            labels = model.fit_predict(part[["value"]])
            part["anomaly"] = labels == -1
            part["anomaly_score"] = -model.decision_function(part[["value"]])
        pieces.append(part)
    return pd.concat(pieces, ignore_index=True) if pieces else frame.assign(anomaly=False, anomaly_score=0.0)


def train_trend_model(frame: pd.DataFrame, benchmark_name: str) -> dict:
    """Train a small baseline regression model from run number to measured value.

    This is a diagnostic trend estimate, not a guarantee of future performance.
    At least 5 valid runs are required.
    """
    subset = frame[frame["name"] == benchmark_name].copy()
    subset["run"] = pd.to_numeric(subset["run"], errors="coerce")
    subset = subset.dropna(subset=["run", "value"]).sort_values("run")
    if len(subset) < 5 or subset["run"].nunique() < 2:
        raise ValueError("At least 5 measurements across 2 or more run numbers are required")
    X, y = subset[["run"]], subset["value"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    next_run = float(X["run"].max() + 1)
    return {"benchmark": benchmark_name, "next_run": next_run,
            "predicted_value": float(model.predict([[next_run]])[0]),
            "mae": float(mean_absolute_error(y_test, predicted)),
            "r2": float(r2_score(y_test, predicted)) if len(y_test) > 1 else None,
            "warning": "Experimental estimate; validate with more repeated measurements."}
