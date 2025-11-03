from aicad.__init__ import compile_all

def test_featurescript_contains_ops():
    out = compile_all("L-bracket 60x40x3 mm, 2 holes")
    fs = out["featurescript"]
    assert "FeatureScript" in fs
    assert "opExtrude" in fs
    assert "skCircle" in fs
