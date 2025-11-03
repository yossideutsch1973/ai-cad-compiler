from __future__ import annotations
from typing import Dict
from .ir import PartSpec, Sketch, Line, Circle, Extrude

def parse_intent(text: str) -> PartSpec:
    """
    Minimal deterministic parser for phrases like:
      "L-bracket 60x40x3 mm, 4 holes (M4) on long leg pitch 10 mm, 1 mm chamfer."
    For v0 we ignore many details and create a base plate with two circles.
    """
    # Heuristic defaults (pure)
    params: Dict[str, float] = {
        "L_long": 60.0, "L_short": 40.0, "thickness": 3.0,
        "hole_d": 4.0, "pitch": 10.0, "chamfer": 1.0
    }
    # One sketch: rectangle outline + two holes as circles (ids e1,e2)
    entities = {
        "e_rect_top": Line(frm=(0, 0), to=(params["L_long"], 0)),
        "e_rect_right": Line(frm=(params["L_long"], 0), to=(params["L_long"], params["L_short"])),
        "e_rect_bottom": Line(frm=(params["L_long"], params["L_short"]), to=(0, params["L_short"])),
        "e_rect_left": Line(frm=(0, params["L_short"]), to=(0, 0)),
        "e1": Circle(center=(params["pitch"], params["L_short"]/2), radius=params["hole_d"]/2),
        "e2": Circle(center=(params["L_long"]-params["pitch"], params["L_short"]/2), radius=params["hole_d"]/2),
    }
    sketches = {"s_base": Sketch(plane="Z", entities=entities, constraints=[])}
    features = [Extrude(sketch_id="s_base", depth=params["thickness"])]
    return PartSpec(name="l_bracket", params=params, sketches=sketches, features=features)
