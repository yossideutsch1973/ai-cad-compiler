from __future__ import annotations
from .ir import PartSpec

def refine_spec(spec: PartSpec) -> PartSpec:
    # v0 is identity; keep place for rules like snapping pitch to grid, min wall, etc.
    return spec
