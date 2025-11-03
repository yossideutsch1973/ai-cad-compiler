from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class KernelCheck:
    ok: bool
    issues: List[str]

def mock_verify_code(_: str) -> KernelCheck:
    # v0 deterministic success; real verification lives in shell-layer adapter.
    return KernelCheck(ok=True, issues=[])
