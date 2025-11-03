from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from aicad import compile_all


@dataclass(frozen=True)
class SuiteResult:
    intent: str
    status: str
    warnings: int


def _load_prompts(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _compile_prompts(prompts: Iterable[str]) -> list[tuple[str, dict]]:
    results: list[tuple[str, dict]] = []
    for intent in prompts:
        results.append((intent, compile_all(intent)))
    return results


def _write_outputs(base: Path, index: int, featurescript: str, cadquery: str) -> None:
    target = base / f"idx_{index:02d}"
    target.mkdir(parents=True, exist_ok=True)
    (target / "part.fs").write_text(featurescript, encoding="utf-8")
    (target / "part.py").write_text(cadquery, encoding="utf-8")


def _summarize(results: Iterable[SuiteResult]) -> tuple[int, int, int]:
    ok = invalid = warnings = 0
    for res in results:
        if res.status == "OK":
            ok += 1
        else:
            invalid += 1
        warnings += res.warnings
    return ok, invalid, warnings


def run_suite(prompts_path: Path, out_dir: Path | None = None) -> list[SuiteResult]:
    prompts = _load_prompts(prompts_path)
    compiled = _compile_prompts(prompts)
    suite_results: list[SuiteResult] = []
    for idx, (intent, payload) in enumerate(compiled, start=1):
        report = payload["report"]
        status = "OK" if report.ok else "INVALID"
        warn_count = len(report.warnings)
        suite_results.append(SuiteResult(intent=intent, status=status, warnings=warn_count))
        if out_dir is not None:
            _write_outputs(out_dir, idx, payload["featurescript"], payload["cadquery"])
    return suite_results


def _print_table(results: Sequence[SuiteResult]) -> None:
    print("idx | status   | warnings | intent")
    print("----+----------+----------+----------------------------------------")
    for idx, res in enumerate(results, start=1):
        print(f"{idx:3d} | {res.status:<8} | {res.warnings:^8d} | {res.intent}")
    ok, invalid, warnings = _summarize(results)
    print()
    print("Summary")
    print(f"  prompts : {len(results)}")
    print(f"  OK      : {ok}")
    print(f"  INVALID : {invalid}")
    print(f"  warnings: {warnings}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a batch of intents through the AI CAD compiler.")
    parser.add_argument("--prompts", default="tests/data/prompts.txt", help="Path to newline-delimited prompts")
    parser.add_argument("--out", default=None, help="Optional output directory for per-intent artifacts")
    args = parser.parse_args(argv)

    prompts_path = Path(args.prompts)
    out_dir = Path(args.out) if args.out else None
    results = run_suite(prompts_path, out_dir)
    _print_table(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
