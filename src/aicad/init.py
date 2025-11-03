from __future__ import annotations
from .dsl_parse import parse_intent
from .refine import refine_spec
from .validate import validate_spec
from .compile_fs import compile_featurescript
from .compile_cadquery import compile_cadquery
from .verify import mock_verify_code
from .compose import pipe

def compile_all(intent: str):
    """
    Pure core: intent -> PartSpec -> (FS, CadQuery) -> static validation.
    Returns a pure dict; any writing/logging is done by shells outside.
    """
    spec = pipe(intent, parse_intent, refine_spec)
    report = validate_spec(spec)
    fs_code = compile_featurescript(spec)
    cq_code = compile_cadquery(spec)
    kernel = mock_verify_code(fs_code)
    return {
        "spec": spec,
        "report": report,
        "featurescript": fs_code,
        "cadquery": cq_code,
        "kernel": kernel
    }
