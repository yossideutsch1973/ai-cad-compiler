from aicad.ir import PartSpec, Sketch
from aicad.dsl_parse import parse_intent
from aicad.refine import refine_spec
from aicad.validate import validate_spec

def test_parse_refine_validate():
    spec = refine_spec(parse_intent("L-bracket 60x40x3 mm"))
    r = validate_spec(spec)
    assert r.ok
    assert isinstance(spec, PartSpec)
    assert "s_base" in spec.sketches
    assert isinstance(spec.sketches["s_base"], Sketch)
