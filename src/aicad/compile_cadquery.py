from __future__ import annotations
from .ir import PartSpec, Line, Circle

def compile_cadquery(spec: PartSpec) -> str:
    """
    Returns a *string* of CadQuery Python code (pure).
    User can run it in a CadQuery/FreeCAD environment as shell-side effect.
    """
    p = spec.params
    L, W, T = p["L_long"], p["L_short"], p["thickness"]
    holes = []
    for eid, ent in spec.sketches["s_base"].entities.items():
        if isinstance(ent, Circle):
            cx, cy = ent.center
            d = ent.radius * 2
            holes.append(f".faces('>Z').workplane().center({cx},{cy}).hole({d})")
    hole_str = "".join(holes)
    return (
f"""import cadquery as cq
result = (
    cq.Workplane("XY")
      .rect({L}, {W})
      .extrude({T})
      {hole_str}
)
# 'result' is the solid. Export outside this pure compiler string.
"""
    )
