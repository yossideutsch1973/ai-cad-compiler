from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .ir import PartSpec

@dataclass(frozen=True)
class Report:
    ok: bool
    errors: List[str]
    warnings: List[str]

def validate_spec(spec: PartSpec) -> Report:
    errs: List[str] = []
    warns: List[str] = []
    p = spec.params
    if p.get("thickness", 0) <= 0:
        errs.append("thickness must be > 0")
    if p.get("L_long", 0) <= 0 or p.get("L_short", 0) <= 0:
        errs.append("dimensions must be > 0")
    if p.get("hole_d", 0) <= 0:
        errs.append("hole_d must be > 0")
    return Report(ok=(len(errs) == 0), errors=errs, warnings=warns)
