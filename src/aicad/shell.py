from __future__ import annotations
from functools import wraps
from typing import Callable, Any, Protocol, Optional

class Sink(Protocol):
    def log(self, msg: str) -> None: ...
    def write_text(self, path: str, text: str) -> None: ...

def with_sink(sink: Sink):
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapped(*args, **kwargs):
            sink.log(f"{fn.__name__} start")
            out = fn(*args, **kwargs)
            sink.log(f"{fn.__name__} end")
            return out
        return wrapped
    return deco

class StdoutSink:
    def __init__(self, writer: Optional[Callable[[str,str],None]] = None):
        self._writer = writer

    def log(self, msg: str) -> None:
        print(msg)

    def write_text(self, path: str, text: str) -> None:
        if self._writer:
            self._writer(path, text)
        else:
            # Default side effect (can be overridden by tests/CI)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
