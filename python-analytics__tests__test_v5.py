from benchart_ai.beam import analyze_simply_supported_beam
from benchart_ai.cfd import analyze_velocity_field
from benchart_ai.model_training import train_tabular_model


def test_beam_udl_reactions_and_moment():
    result = analyze_simply_supported_beam(4, "udl", 1000)
    assert result["left_reaction_n"] == 2000
    assert result["right_reaction_n"] == 2000
    assert result["max_bending_moment_nm"] == 2000


def test_beam_midspan_point_load():
    result = analyze_simply_supported_beam(6, "midspan_point", 1200)
    assert result["left_reaction_n"] == 600
    assert result["max_bending_moment_nm"] == 1800


def test_cfd_velocity_magnitude():
    result = analyze_velocity_field([{"x": 0, "y": 0, "u": 3, "v": 4}])
    assert result["max_speed"] == 5


def test_ml_regression_training():
    rows = [{"feature": i, "target": 2 * i + 1} for i in range(20)]
    result = train_tabular_model(rows, "target")
    assert result["rows_used"] == 20
    assert "rmse" in result["metrics"]
