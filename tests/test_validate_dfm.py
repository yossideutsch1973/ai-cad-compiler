from __future__ import annotations

from aicad.ir import PartSpec
from aicad.validate import validate_spec


def _make_spec(**overrides):
    params = {
        "thickness": 3.0,
        "L_long": 60.0,
        "L_short": 40.0,
        "hole_d": 4.0,
    }
    params.update(overrides)
    return PartSpec(name="demo", params=params, sketches={}, features=[])


def test_warns_for_thin_wall():
    report = validate_spec(_make_spec(thickness=1.5))
    assert report.ok
    assert any("wall thickness" in warning for warning in report.warnings)


def test_warns_for_small_drill():
    report = validate_spec(_make_spec(hole_d=2.0))
    assert report.ok
    assert any("hole diameter" in warning for warning in report.warnings)


def test_warns_for_extreme_aspect_ratio():
    report = validate_spec(_make_spec(L_long=200.0, L_short=10.0))
    assert report.ok
    assert any("aspect ratio" in warning for warning in report.warnings)
