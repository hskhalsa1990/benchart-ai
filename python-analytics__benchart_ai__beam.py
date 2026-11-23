from __future__ import annotations
import numpy as np


def analyze_simply_supported_beam(span_m: float, load_type: str, load_value: float, points: int = 101, elastic_modulus_gpa: float | None = None, second_moment_m4: float | None = None):
    """Euler-Bernoulli beam diagrams for a simply-supported beam with UDL or a midspan point load."""
    if span_m <= 0 or load_value < 0 or points < 11:
        raise ValueError("span_m must be positive, load_value non-negative, and points at least 11")
    x = np.linspace(0.0, span_m, points)
    if load_type == "udl":
        w = load_value  # N/m
        reaction = w * span_m / 2
        shear = reaction - w * x
        moment = reaction * x - w * x**2 / 2
        max_moment = w * span_m**2 / 8
        max_deflection = None
        if elastic_modulus_gpa is not None or second_moment_m4 is not None:
            if not elastic_modulus_gpa or not second_moment_m4 or elastic_modulus_gpa <= 0 or second_moment_m4 <= 0:
                raise ValueError("Provide positive elastic_modulus_gpa and second_moment_m4 together")
            max_deflection = 5 * w * span_m**4 / (384 * elastic_modulus_gpa * 1e9 * second_moment_m4)
    elif load_type == "midspan_point":
        p = load_value  # N
        reaction = p / 2
        shear = np.where(x < span_m/2, reaction, np.where(x > span_m/2, -reaction, 0.0))
        moment = np.where(x <= span_m/2, reaction*x, reaction*(span_m-x))
        max_moment = p * span_m / 4
        max_deflection = None
        if elastic_modulus_gpa is not None or second_moment_m4 is not None:
            if not elastic_modulus_gpa or not second_moment_m4 or elastic_modulus_gpa <= 0 or second_moment_m4 <= 0:
                raise ValueError("Provide positive elastic_modulus_gpa and second_moment_m4 together")
            max_deflection = p * span_m**3 / (48 * elastic_modulus_gpa * 1e9 * second_moment_m4)
    else:
        raise ValueError("load_type must be 'udl' or 'midspan_point'")
    return {"model":"simply_supported_euler_bernoulli_beam", "load_type":load_type, "span_m":span_m,
            "left_reaction_n":reaction, "right_reaction_n":reaction, "max_bending_moment_nm":float(max_moment),
            "max_deflection_m":float(max_deflection) if max_deflection is not None else None,
            "diagram":[{"x_m":float(a),"shear_n":float(b),"moment_nm":float(c)} for a,b,c in zip(x,shear,moment)],
            "assumptions":["linear elastic Euler-Bernoulli beam", "simply supported ends", "point load at midspan or full-span UDL", "small deflection"]}
