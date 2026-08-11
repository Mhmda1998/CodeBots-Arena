"""
Sandbox runner — executes untrusted bot code in a restricted environment.
Uses RestrictedPython for safe AST-level execution.
"""
from __future__ import annotations

import multiprocessing
import os
from typing import Any

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_globals


SAFE_BUILTINS = {
    "abs", "all", "any", "bool", "dict", "enumerate", "filter", "float",
    "int", "isinstance", "issubclass", "len", "list", "map", "max", "min",
    "print", "range", "repr", "reversed", "round", "set", "sorted", "str",
    "sum", "tuple", "type", "zip", "True", "False", "None",
}


def safe_exec(code: str, max_runtime_s: float = 2.0) -> dict[str, Any]:
    """
    Safely execute a bot's init code and return the namespace.
    Raises RuntimeError on timeout, syntax error, or unsafe code.
    """
    try:
        byte_code = compile_restricted(code, filename="<bot>", mode="exec")
    except SyntaxError as e:
        raise RuntimeError(f"Syntax error: {e}")

    safe_globals_copy = dict(safe_globals)
    builtins_dict = getattr(__builtins__, "__dict__", {}) if hasattr(__builtins__, "__dict__") else dict(__builtins__)
    safe_globals_copy["__builtins__"] = {k: builtins_dict[k] for k in SAFE_BUILTINS if k in builtins_dict}

    def _target(q: multiprocessing.Queue) -> None:
        try:
            namespace: dict = {"__name__": "__bot__"}
            exec(byte_code, safe_globals_copy, namespace)  # noqa: S102
            q.put(("ok", namespace))
        except Exception as e:
            q.put(("err", str(e)))

    q: multiprocessing.Queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_target, args=(q,), daemon=True)
    p.start()
    p.join(timeout=max_runtime_s)
    if p.is_alive():
        p.terminate()
        p.join()
        raise RuntimeError("Bot init took too long (timeout)")
    if q.empty():
        raise RuntimeError("Bot init produced no output")
    status, value = q.get()
    if status == "err":
        raise RuntimeError(f"Bot init failed: {value}")
    return value
