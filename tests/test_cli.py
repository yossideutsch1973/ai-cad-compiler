from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_cli_generates_outputs(tmp_path: Path) -> None:
    out_dir = tmp_path / "artifacts"
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    src_path = str(Path(__file__).resolve().parents[1] / "src")
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [src_path, existing]))
    result = subprocess.run(
        [sys.executable, "-m", "aicad.cli", "L-bracket 60x40x3 mm", "--out", str(out_dir)],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    stdout_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert stdout_lines[-1] == "OK"
    assert (out_dir / "part.fs").exists()
    assert (out_dir / "part.py").exists()
