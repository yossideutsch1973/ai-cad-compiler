from __future__ import annotations
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def pipe(x: A, *funcs: Callable[[A], B]) -> B:
    out = x
    for f in funcs:
        out = f(out)  # type: ignore
    return out  # type: ignore

def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: f(g(x))
