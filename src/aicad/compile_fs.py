from __future__ import annotations
from typing import List
from .ir import PartSpec, Line, Circle

def _fs_header(name: str) -> str:
    return (
        "FeatureScript 2200;\n"
        f"annotation {name} is AnnotatedType<{}>;\n"
        "export const GEN_PART = defineFeature(function(ctx is Context, id is Id, def is map)\n"
        "{\n"
        "    var sk = newSketchOnPlane(ctx, id + 'sk', {\"plane\" : plane(plane.ZY)});\n"
    )

def _fs_entities(spec: PartSpec) -> List[str]:
    lines: List[str] = []
    s = spec.sketches["s_base"]
    for eid, ent in s.entities.items():
        if isinstance(ent, Line):
            (x1, y1), (x2, y2) = ent.frm, ent.to
            lines.append(f"    skLineSegment(sk, vector({x1}*millimeter,{y1}*millimeter), vector({x2}*millimeter,{y2}*millimeter));\n")
        elif isinstance(ent, Circle):
            (cx, cy), r = ent.center, ent.radius
            lines.append(f"    skCircle(sk, vector({cx}*millimeter,{cy}*millimeter), {r}*millimeter);\n")
    return lines

def _fs_footer(depth_mm: float) -> str:
    return (
        "    skSolve(sk);\n"
        "    opExtrude(ctx, id + 'ext', {\n"
        "        'entities' : qSketchRegion(id + 'sk'),\n"
        f"        'endBound' : BoundingType.BLIND,\n"
        f"        'endDepth' : {depth_mm}*millimeter\n"
        "    });\n"
        "});\n"
    )

def compile_featurescript(spec: PartSpec) -> str:
    depth = float(spec.params.get("thickness", 3.0))
    return _fs_header(spec.name) + "".join(_fs_entities(spec)) + _fs_footer(depth)
