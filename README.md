# AI-CAD Compiler

A **pure-function pipeline** that turns natural language design intents into parametric CAD models.  
It generates both **Onshape FeatureScript** and **CadQuery (FreeCAD-friendly)** code from a clean,
deterministic intermediate representation (IR).  
All side effects (logging, file I/O, kernel checks) are isolated in decorator shells.

**🌐 [Try the Live Demo](https://yossideutsch1973.github.io/ai-cad-compiler/)** - Run the compiler directly in your browser!

---

## ✨ Core Philosophy

- **Pure functions only:** every transformation is referentially transparent.  
- **Decorated shell:** any I/O (saving files, invoking kernels) is added externally through decorators.  
- **Deterministic IR:** all geometry is expressed through simple, typed dataclasses.  
- **Composable design:** functional composition (`pipe`, `compose`) connects each stage.  
- **Dual backends:** the same IR compiles to Onshape FeatureScript and CadQuery Python.

---

## 📦 Directory Layout

ai-cad-compiler/
├─ README.md
├─ pyproject.toml
├─ src/
│  └─ aicad/
│     ├─ init.py           # compose full pipeline
│     ├─ ir.py                 # type-safe intermediate representation
│     ├─ dsl_parse.py          # text → IR draft
│     ├─ refine.py             # deterministic adjustments
│     ├─ validate.py           # static rule checks
│     ├─ compile_fs.py         # FeatureScript backend
│     ├─ compile_cadquery.py   # CadQuery backend
│     ├─ verify.py             # mock kernel verifier
│     ├─ compose.py            # functional composition helpers
│     └─ shell.py              # decorator layer for I/O/logging
└─ tests/
├─ test_ir_roundtrip.py
├─ test_bracket_fs.py
└─ data/
└─ prompts.txt

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourname/ai-cad-compiler.git
cd ai-cad-compiler
pip install -e .
pytest -q
```

## CLI & Suite

```bash
aicad "L-bracket 60x40x3 mm, 2 holes M4 pitch 10" --out out
python tools/run_suite.py --prompts tests/data/prompts.txt --out out/suite
```

⸻

🧠 Usage

from aicad import compile_all

res = compile_all("L-bracket 60x40x3 mm, 2 holes M4 pitch 10 mm")

print(res["featurescript"])  # Onshape FeatureScript source
print(res["cadquery"])       # CadQuery Python source
print(res["report"])         # Validation result

The output contains no side effects — pure strings and dataclasses only.

⸻

🧩 Composition Model

Each stage is a pure function:

intent
  └─ parse_intent(text)       # rule-based or LLM-based
     └─ refine_spec(spec)     # normalize parameters, enforce units
        └─ validate_spec(spec)→ Report
           ├─ compile_featurescript(spec)
           ├─ compile_cadquery(spec)
           └─ verify_kernel(code) → KernelCheck

The outer shell (StdoutSink or custom) adds logging, saving, or kernel invocation.

⸻

🧱 Example Output (FeatureScript)

FeatureScript 2200;
annotation l_bracket is AnnotatedType<{}>;
export const GEN_PART = defineFeature(function(ctx is Context, id is Id, def is map)
{
    var sk = newSketchOnPlane(ctx, id + 'sk', {"plane" : plane(plane.ZY)});
    skLineSegment(sk, vector(0*millimeter,0*millimeter), vector(60*millimeter,0*millimeter));
    skCircle(sk, vector(10*millimeter,20*millimeter), 2*millimeter);
    skSolve(sk);
    opExtrude(ctx, id + 'ext', {
        'entities' : qSketchRegion(id + 'sk'),
        'endBound' : BoundingType.BLIND,
        'endDepth' : 3*millimeter
    });
});


⸻

🧪 Tests

pytest -q

Sample assertions ensure the parser, validator, and compilers produce deterministic results.

⸻

🛠️ Extending
	1.	Add DFM linting: thickness, drill size, min wall, bend radius.
	2.	Integrate kernels: wrap verify.py with real Onshape/FreeCAD checks inside a decorator.
	3.	Enhance DSL: train a prompt-to-IR LLM using SketchGraphs or Fusion 360 Gallery datasets.
	4.	Generate assemblies: extend PartSpec with mates and constraints.

⸻

🧃 Philosophy in One Line

Pure functions build truth; decorators talk to the world.

⸻

🗂 License

MIT License — feel free to reuse, remix, or embed into your own CAD workflows.

⸻

🧰 Credits

Developed as part of an AI-CAD functional-core experiment using Codex-5
and guided by the principle that design should be composable, verifiable, and fun.

