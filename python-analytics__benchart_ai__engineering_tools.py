"""Lightweight engineering calculators. Educational/preliminary sizing only."""
from __future__ import annotations
import itertools
import math
import pandas as pd

MATERIALS = {
    "steel_1045": {"name": "AISI 1045 steel (typical)", "density_kg_m3": 7850, "youngs_modulus_gpa": 205, "yield_strength_mpa": 530, "poisson_ratio": 0.29},
    "al_6061_t6": {"name": "Aluminium 6061-T6 (typical)", "density_kg_m3": 2700, "youngs_modulus_gpa": 68.9, "yield_strength_mpa": 276, "poisson_ratio": 0.33},
    "stainless_304": {"name": "Stainless steel 304 (typical)", "density_kg_m3": 8000, "youngs_modulus_gpa": 193, "yield_strength_mpa": 215, "poisson_ratio": 0.29},
    "titanium_grade5": {"name": "Ti-6Al-4V Grade 5 (typical)", "density_kg_m3": 4430, "youngs_modulus_gpa": 114, "yield_strength_mpa": 880, "poisson_ratio": 0.34},
}

def unit_convert(value: float, quantity: str, from_unit: str, to_unit: str) -> dict:
    tables = {
        "length": {"m": 1, "mm": 1e-3, "cm": 1e-2, "km": 1e3, "in": .0254, "ft": .3048},
        "force": {"N": 1, "kN": 1e3, "lbf": 4.4482216153},
        "pressure": {"Pa": 1, "kPa": 1e3, "MPa": 1e6, "GPa": 1e9, "bar": 1e5, "psi": 6894.757293},
        "mass": {"kg": 1, "g": 1e-3, "tonne": 1e3, "lb": .45359237},
        "energy": {"J": 1, "kJ": 1e3, "Wh": 3600, "kWh": 3.6e6},
        "power": {"W": 1, "kW": 1e3, "hp": 745.699872},
        "speed": {"m/s": 1, "km/h": 1/3.6, "mph": .44704},
        "temperature": {"C": "C", "F": "F", "K": "K"},
    }
    if quantity not in tables or from_unit not in tables[quantity] or to_unit not in tables[quantity]:
        raise ValueError("Unsupported quantity or unit pair")
    if quantity == "temperature":
        c = value if from_unit == "C" else (value-32)*5/9 if from_unit == "F" else value-273.15
        out = c if to_unit == "C" else c*9/5+32 if to_unit == "F" else c+273.15
    else:
        out = value * tables[quantity][from_unit] / tables[quantity][to_unit]
    return {"quantity": quantity, "input": value, "from_unit": from_unit, "result": out, "to_unit": to_unit}

def shaft_torsion(torque_nm: float, diameter_mm: float, length_mm: float, shear_modulus_gpa: float = 79.3) -> dict:
    if torque_nm < 0 or diameter_mm <= 0 or length_mm < 0 or shear_modulus_gpa <= 0:
        raise ValueError("Torque must be non-negative; dimensions and shear modulus must be positive")
    d, T, G, L = diameter_mm/1000, torque_nm, shear_modulus_gpa*1e9, length_mm/1000
    tau = 16*T/(math.pi*d**3) if T else 0
    theta = T*L/(G*(math.pi*d**4/32))
    return {"max_shear_stress_mpa": tau/1e6, "twist_angle_deg": math.degrees(theta), "polar_moment_m4": math.pi*d**4/32, "scope": "solid circular shaft, elastic torsion theory"}

def goodman_check(sigma_a_mpa: float, sigma_m_mpa: float, endurance_limit_mpa: float, ultimate_strength_mpa: float) -> dict:
    if min(sigma_a_mpa, endurance_limit_mpa, ultimate_strength_mpa) <= 0 or ultimate_strength_mpa <= sigma_m_mpa:
        raise ValueError("Stress amplitude, endurance limit and ultimate strength must be positive; mean stress must be below ultimate strength")
    utilization = sigma_a_mpa/endurance_limit_mpa + sigma_m_mpa/ultimate_strength_mpa
    return {"goodman_utilization": utilization, "factor_of_safety": (1/utilization if utilization > 0 else None), "passes_at_fos_1": utilization <= 1, "scope": "modified Goodman criterion; verify material, notch and surface factors"}

def factorial_design(factors: dict[str, list[float]], center_points: int = 0) -> dict:
    if not factors or len(factors) > 8 or any(not isinstance(v, list) or len(v) != 2 or v[0] == v[1] for v in factors.values()):
        raise ValueError("Provide 1–8 factors, each with exactly two distinct low/high values")
    if center_points < 0 or center_points > 100:
        raise ValueError("center_points must be between 0 and 100")
    names = list(factors)
    rows = [dict(zip(names, values)) for values in itertools.product(*[factors[n] for n in names])]
    if center_points:
        center = {n: (float(factors[n][0])+float(factors[n][1]))/2 for n in names}
        rows.extend([center.copy() for _ in range(center_points)])
    return {"design": "full_factorial_2_level", "factor_count": len(names), "run_count": len(rows), "factors": names, "runs": rows}

def correlation_matrix(rows: list[dict]) -> dict:
    frame = pd.DataFrame(rows).select_dtypes(include="number")
    if len(frame) < 2 or frame.shape[1] < 2:
        raise ValueError("Need at least two rows and two numeric columns")
    return {"columns": list(frame.columns), "correlation": frame.corr(numeric_only=True).round(6).where(pd.notna(frame.corr(numeric_only=True)), None).to_dict(), "rows_used": int(len(frame))}
