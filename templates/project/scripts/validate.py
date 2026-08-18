"""Continuous validation helper (standard library only).

Every analysis step whose expected shape is known in advance asserts it here, immediately after the
step runs. The expected value must come from outside the code that produced the object (an
annotation file, a sample sheet, a published n), otherwise the check passes by construction.

Usage:
    from validate import check, init, summary

    init("results/checks", step="01_load_counts")
    check("annotated transcripts", len(df), 50000, source="GENCODE v44 GTF")
    check("samples retained", df.sample_id.nunique(), 24, source="samplesheet.csv")
    check("IDs preserved after join", set(df.id) == set(ref.id), True)
    summary()

A failed check raises ValidationError. Nothing downstream should execute on data of the wrong shape.
"""

from __future__ import annotations

import os
from datetime import datetime
from numbers import Number
from typing import Any

__all__ = ["ValidationError", "init", "check", "summary"]


class ValidationError(AssertionError):
    """Raised when an observed value does not match the value expected in advance."""


_state: dict[str, Any] = {"log": None, "tsv": None, "step": "", "pass": 0, "fail": 0}


def init(prefix: str = "results/checks", step: str = "", append: bool = False) -> str:
    """Start a validation log.

    Writes ``<prefix>.log`` (human readable) and ``<prefix>.tsv`` (machine readable, read by the
    write-up and review steps). ``step`` is recorded on every line.
    """
    directory = os.path.dirname(prefix)
    if directory:
        os.makedirs(directory, exist_ok=True)
    _state.update(log=f"{prefix}.log", tsv=f"{prefix}.tsv", step=step)
    _state["pass"] = 0
    _state["fail"] = 0
    if not append or not os.path.exists(_state["tsv"]):
        open(_state["log"], "w").close()
        with open(_state["tsv"], "w") as fh:
            fh.write("status\ttimestamp\tstep\tlabel\tactual\texpected\tsource\n")
    _write(f"=== validation: {step or 'analysis'} ({_now()}) ===")
    return prefix


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _write(line: str) -> None:
    print(line)
    if _state["log"]:
        with open(_state["log"], "a") as fh:
            fh.write(line + "\n")


def _fmt(value: Any) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,.0f}" if value == int(value) else f"{value:,.6g}"
    text = str(value)
    return text if len(text) <= 80 else text[:77] + "..."


def check(
    label: str,
    actual: Any,
    expected: Any,
    tol: float = 0,
    source: str = "",
    warn_only: bool = False,
) -> bool:
    """Assert one expected value and record the result.

    ``label`` is a plain-language description, ``actual`` the observed value, ``expected`` the value
    known in advance (use ``True`` for logical assertions), ``tol`` an absolute numeric tolerance,
    and ``source`` where the expected value came from. ``warn_only`` records a mismatch as WARN and
    continues: use it only for informational counts, never for a shape downstream code depends on.
    """
    if _state["log"] is None:
        init()

    if isinstance(expected, bool):
        ok = bool(actual) is expected
    elif isinstance(expected, Number) and isinstance(actual, Number):
        # Guard the comparison against binary floating-point representation error, so a value
        # exactly on the tolerance boundary (0.51 against 0.50 +/- 0.01) passes.
        slack = tol * 1e-9 + abs(float(expected)) * 1e-12
        ok = abs(float(actual) - float(expected)) <= tol + slack
    else:
        ok = actual == expected

    status = "PASS" if ok else ("WARN" if warn_only else "FAIL")
    timestamp = _now()
    detail = f"{label}: {_fmt(actual)} (expected {_fmt(expected)}"
    detail += f" +/- {_fmt(tol)})" if tol else ")"
    if source:
        detail += f"  [{source}]"
    _write(f"{status:<4} {timestamp}  {detail}")

    if _state["tsv"]:
        with open(_state["tsv"], "a") as fh:
            fh.write(
                "\t".join(
                    [status, timestamp, _state["step"], label, _fmt(actual), _fmt(expected), source]
                )
                + "\n"
            )

    if ok:
        _state["pass"] += 1
    else:
        _state["fail"] += 1
        if not warn_only:
            raise ValidationError(f"Validation failed | {detail}")
    return ok


def summary() -> dict[str, int]:
    """Close the log with a one-line tally and return the counts."""
    total = _state["pass"] + _state["fail"]
    _write(f"--- {total} checks: {_state['pass']} passed, {_state['fail']} failed ---")
    return {"pass": _state["pass"], "fail": _state["fail"]}
