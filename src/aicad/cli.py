from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from . import compile_all
from .shell import StdoutSink


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile an AI CAD intent into FeatureScript and CadQuery outputs.")
    parser.add_argument("intent", help="Natural language description of the part")
    parser.add_argument("--out", default="out", help="Output directory for generated files")
    return parser.parse_args(argv)


def _write_outputs(out_dir: Path, featurescript: str, cadquery: str, sink: StdoutSink) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    sink.write_text(str(out_dir / "part.fs"), featurescript)
    sink.write_text(str(out_dir / "part.py"), cadquery)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    result = compile_all(args.intent)
    sink = StdoutSink()
    output_dir = Path(args.out)
    _write_outputs(output_dir, result["featurescript"], result["cadquery"], sink)
    status = "OK" if result["report"].ok else "INVALID"
    print(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
