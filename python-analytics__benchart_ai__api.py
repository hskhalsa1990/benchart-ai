from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import pandas as pd
from .cleaning import clean_benchmark_frame
from .statistics import summarize, compare_groups
from .ml import detect_anomalies

app = FastAPI(title="Benchart AI Analytics API", version="0.5.0",
              description="Optional Python analytics companion for Benchart benchmark data")

class BenchmarkPayload(BaseModel):
    rows: list[dict] = Field(..., min_length=1, description="Rows with name, value and optional group/unit/run")

class ComparePayload(BenchmarkPayload):
    baseline: str
    candidate: str


def to_frame(payload: BenchmarkPayload) -> pd.DataFrame:
    try:
        return clean_benchmark_frame(pd.DataFrame(payload.rows))
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.get("/health")
def health():
    return {"status": "ok", "service": "benchart-ai"}

@app.post("/analyze")
def analyze(payload: BenchmarkPayload):
    frame = to_frame(payload)
    return summarize(frame)

@app.post("/compare")
def compare(payload: ComparePayload):
    frame = to_frame(payload)
    try:
        return {"comparison": compare_groups(frame, payload.baseline, payload.candidate)}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/anomalies")
def anomalies(payload: BenchmarkPayload):
    frame = to_frame(payload)
    return {"rows": detect_anomalies(frame).to_dict(orient="records")}


# Integrated platform endpoints
from .fea import analyze_fea
from .deep_learning import backend_status
from pydantic import BaseModel

class FEARequest(BaseModel):
    rows: list[dict] = Field(..., min_length=1)
    yield_strength_mpa: float | None = None

@app.get("/deep-learning/status")
def deep_learning_status():
    return backend_status()

@app.post("/fea/analyze")
def fea_analyze(payload: FEARequest):
    try:
        return analyze_fea(payload.rows, payload.yield_strength_mpa)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


# Dashboard assets are served alongside the API.
_DASHBOARD_DIR = Path(__file__).resolve().parents[2] / "dashboard"
if _DASHBOARD_DIR.exists():
    app.mount("/dashboard", StaticFiles(directory=str(_DASHBOARD_DIR), html=True), name="dashboard")

@app.get("/", include_in_schema=False)
def dashboard_home():
    return RedirectResponse(url="/dashboard/")


# Cross-discipline platform endpoints (demonstration / post-processing scope is stated per module).
import math
from pathlib import Path as _Path

@app.get("/platform/modules")
def platform_modules():
    modules_file = _Path(__file__).resolve().parents[2] / "dashboard" / "modules.json"
    return {"modules": __import__("json").loads(modules_file.read_text(encoding="utf-8"))}

class RoboticsRequest(BaseModel):
    joint1_deg: float = 30
    joint2_deg: float = 45
    link1: float = 1.0
    link2: float = 0.8

@app.post("/robotics/forward-kinematics")
def robotics_forward_kinematics(payload: RoboticsRequest):
    if payload.link1 <= 0 or payload.link2 <= 0:
        raise HTTPException(status_code=422, detail="Link lengths must be positive")
    a1, a2 = math.radians(payload.joint1_deg), math.radians(payload.joint2_deg)
    x = payload.link1*math.cos(a1) + payload.link2*math.cos(a1+a2)
    y = payload.link1*math.sin(a1) + payload.link2*math.sin(a1+a2)
    return {"x": x, "y": y, "joint1_deg": payload.joint1_deg, "joint2_deg": payload.joint2_deg, "units": "same as link lengths"}

class DataProfileRequest(BaseModel):
    rows: list[dict] = Field(..., min_length=1)

@app.post("/data-science/profile")
def data_science_profile(payload: DataProfileRequest):
    frame = pd.DataFrame(payload.rows)
    return {"rows": int(len(frame)), "columns": int(len(frame.columns)), "missing_by_column": frame.isna().sum().to_dict(), "numeric_summary": frame.describe(include="number").replace({float("nan"): None}).to_dict(), "column_types": {k: str(v) for k,v in frame.dtypes.items()}}

# v5 engineering calculations and supervised ML workflow
from .beam import analyze_simply_supported_beam
from .cfd import analyze_velocity_field
from .model_training import train_tabular_model

class BeamRequest(BaseModel):
    span_m: float = Field(gt=0)
    load_type: str = Field(pattern="^(udl|midspan_point)$")
    load_value: float = Field(ge=0)
    points: int = Field(default=101, ge=11, le=1001)
    elastic_modulus_gpa: float | None = Field(default=None, gt=0)
    second_moment_m4: float | None = Field(default=None, gt=0)

@app.post("/engineering/beam/analyze")
def beam_analyze(payload: BeamRequest):
    try:
        return analyze_simply_supported_beam(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

class CFDRequest(BaseModel):
    rows: list[dict] = Field(..., min_length=1)

@app.post("/cfd/analyze-field")
def cfd_analyze(payload: CFDRequest):
    try:
        return analyze_velocity_field(payload.rows)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

class TrainRequest(BaseModel):
    rows: list[dict] = Field(..., min_length=8)
    target: str
    task: str = Field(default="regression", pattern="^(regression|classification)$")
    test_size: float = Field(default=0.25, gt=0.05, lt=0.5)

@app.post("/ml/train-tabular")
def ml_train(payload: TrainRequest):
    try:
        return train_tabular_model(payload.rows, payload.target, payload.task, payload.test_size)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

# v6 engineering toolbox: unit conversion, materials, shaft sizing, fatigue and DOE.
from .engineering_tools import MATERIALS, unit_convert, shaft_torsion, goodman_check, factorial_design, correlation_matrix

class UnitConvertRequest(BaseModel):
    value: float
    quantity: str
    from_unit: str
    to_unit: str

@app.post('/tools/unit-convert')
def tools_unit_convert(payload: UnitConvertRequest):
    try:
        return unit_convert(payload.value, payload.quantity, payload.from_unit, payload.to_unit)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.get('/engineering/materials')
def engineering_materials():
    return {'materials': MATERIALS, 'notice': 'Typical reference values only; confirm certified datasheets and condition.'}

class ShaftRequest(BaseModel):
    torque_nm: float = Field(ge=0)
    diameter_mm: float = Field(gt=0)
    length_mm: float = Field(ge=0)
    shear_modulus_gpa: float = Field(default=79.3, gt=0)

@app.post('/engineering/shaft/torsion')
def engineering_shaft(payload: ShaftRequest):
    try:
        return shaft_torsion(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

class GoodmanRequest(BaseModel):
    sigma_a_mpa: float = Field(gt=0)
    sigma_m_mpa: float
    endurance_limit_mpa: float = Field(gt=0)
    ultimate_strength_mpa: float = Field(gt=0)

@app.post('/engineering/fatigue/goodman')
def engineering_goodman(payload: GoodmanRequest):
    try:
        return goodman_check(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

class DOERequest(BaseModel):
    factors: dict[str, list[float]]
    center_points: int = Field(default=0, ge=0, le=100)

@app.post('/data-science/doe/full-factorial')
def data_science_doe(payload: DOERequest):
    try:
        return factorial_design(payload.factors, payload.center_points)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

class CorrelationRequest(BaseModel):
    rows: list[dict] = Field(..., min_length=2)

@app.post('/data-science/correlation')
def data_science_correlation(payload: CorrelationRequest):
    try:
        return correlation_matrix(payload.rows)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
