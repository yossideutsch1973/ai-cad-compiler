# AI-CAD Compiler (pure core + decorator shell)

**Goal:** Deterministic, pure-function pipeline from language -> IR -> CAD backends
(Onshape FeatureScript, CadQuery) with all I/O isolated in decorators.

## Quick start

```bash
pip install -e .
pytest -q
