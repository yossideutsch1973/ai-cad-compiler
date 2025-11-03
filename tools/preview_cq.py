from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def _cadquery_available() -> bool:
    try:
        import cadquery  # type: ignore[unused-import]
    except Exception:
        return False
    return True


def _export_step(script_path: Path, out_path: Path) -> None:
    command = (
        "import cadquery as cq, pathlib, sys\n"
        "script = pathlib.Path(sys.argv[1])\n"
        "out_path = pathlib.Path(sys.argv[2])\n"
        "code = script.read_text(encoding='utf-8')\n"
        "namespace: dict[str, object] = {}\n"
        "exec(compile(code, str(script), 'exec'), namespace)\n"
        "model = namespace.get('result')\n"
        "if model is None:\n"
        "    raise SystemExit('generated script did not define a `result` solid')\n"
        "out_path.parent.mkdir(parents=True, exist_ok=True)\n"
        "cq.exporters.export(model, str(out_path))\n"
    )
    subprocess.run(
        [sys.executable, "-c", command, str(script_path), str(out_path)],
        check=True,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preview a CadQuery part by exporting a STEP file.")
    parser.add_argument("path", help="Path to the generated CadQuery Python file")
    parser.add_argument("--out", default="out/part.step", help="Destination STEP file path")
    args = parser.parse_args(argv)

    script_path = Path(args.path)
    out_path = Path(args.out)

    if not _cadquery_available():
        print("CadQuery not installed; skipping STEP export.")
        return 0

    try:
        _export_step(script_path, out_path)
    except subprocess.CalledProcessError as exc:
        print(f"Failed to export STEP via CadQuery: {exc}")
        return exc.returncode or 1

    print(f"Exported STEP model to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
