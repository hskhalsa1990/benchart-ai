from benchart_ai.engineering_tools import unit_convert, shaft_torsion, goodman_check, factorial_design, correlation_matrix

def test_unit_convert():
    assert abs(unit_convert(1000, 'length', 'mm', 'm')['result'] - 1) < 1e-12

def test_shaft_torsion():
    r = shaft_torsion(100, 20, 500)
    assert r['max_shear_stress_mpa'] > 0 and r['twist_angle_deg'] > 0

def test_goodman():
    r = goodman_check(50, 30, 150, 600)
    assert r['factor_of_safety'] > 1

def test_doe():
    r = factorial_design({'a': [1, 2], 'b': [10, 20]}, 2)
    assert r['run_count'] == 6

def test_correlation():
    r = correlation_matrix([{'x': 1, 'y': 2}, {'x': 2, 'y': 4}, {'x': 3, 'y': 6}])
    assert r['correlation']['x']['y'] == 1.0
