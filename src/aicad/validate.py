from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .ir import PartSpec

_MIN_WALL_MM = 2.0
_MIN_DRILL_MM = 2.5
_MAX_PLATE_ASPECT = 10.0


@dataclass(frozen=True)
class Report:
    ok: bool
    errors: List[str]
    warnings: List[str]


def _lint_wall(thickness: float, warnings: List[str]) -> None:
    if 0 < thickness < _MIN_WALL_MM:
        warnings.append(
            f"wall thickness {thickness} mm below {_MIN_WALL_MM} mm minimum"
        )


def _lint_drill(hole_d: float, warnings: List[str]) -> None:
    if 0 < hole_d < _MIN_DRILL_MM:
        warnings.append(
            f"hole diameter {hole_d} mm below {_MIN_DRILL_MM} mm minimum drill size"
        )


def _lint_aspect(long_dim: float, short_dim: float, warnings: List[str]) -> None:
    if long_dim > 0 and short_dim > 0:
        ratio = long_dim / short_dim
        if ratio > _MAX_PLATE_ASPECT:
            warnings.append(
                f"plate aspect ratio {ratio:.1f} exceeds {_MAX_PLATE_ASPECT:.1f} limit"
            )


def validate_spec(spec: PartSpec) -> Report:
    errs: List[str] = []
    warns: List[str] = []
    params = spec.params

    thickness = params.get("thickness", 0)
    if thickness <= 0:
        errs.append("thickness must be > 0")
    else:
        _lint_wall(thickness, warns)

    long_dim = params.get("L_long", 0)
    short_dim = params.get("L_short", 0)
    if long_dim <= 0 or short_dim <= 0:
        errs.append("dimensions must be > 0")
    else:
        _lint_aspect(max(long_dim, short_dim), min(long_dim, short_dim), warns)

    hole_d = params.get("hole_d", 0)
    if hole_d <= 0:
        errs.append("hole_d must be > 0")
    else:
        _lint_drill(hole_d, warns)

    return Report(ok=(len(errs) == 0), errors=errs, warnings=warns)
