"""Tests for the Python validation helper. Run: python3 -m pytest test_validate.py -q"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "templates", "project", "scripts"))

from validate import ValidationError, check, init, summary  # noqa: E402


@pytest.fixture()
def log(tmp_path):
    prefix = str(tmp_path / "checks")
    init(prefix, step="test")
    return prefix


def test_exact_pass_writes_readable_line(log):
    assert check("transcripts", 50000, 50000, source="GENCODE v44") is True
    text = open(log + ".log").read()
    assert "PASS" in text
    assert "transcripts: 50,000 (expected 50,000)" in text
    assert "[GENCODE v44]" in text


def test_mismatch_stops_the_run(log):
    with pytest.raises(ValidationError):
        check("transcripts", 49999, 50000)
    assert "FAIL" in open(log + ".log").read()


def test_off_by_one_is_a_failure_not_a_rounding_pass(log):
    with pytest.raises(ValidationError):
        check("samples", 23, 24)


def test_tolerance_band_edges(log):
    assert check("proportion", 0.51, 0.50, tol=0.01)
    with pytest.raises(ValidationError):
        check("proportion", 0.52, 0.50, tol=0.01)


def test_logical_assertion(log):
    assert check("ids preserved", {1, 2} == {1, 2}, True)
    with pytest.raises(ValidationError):
        check("ids preserved", {1, 2} == {1, 3}, True)


def test_zero_actual_is_not_silently_truthy(log):
    with pytest.raises(ValidationError):
        check("cells retained", 0, 5000)


def test_warn_only_records_but_continues(log):
    assert check("optional count", 5, 6, warn_only=True) is False
    assert "WARN" in open(log + ".log").read()


def test_tsv_is_machine_readable(log):
    check("transcripts", 50000, 50000, source="GENCODE v44")
    rows = open(log + ".tsv").read().strip().split("\n")
    assert rows[0].split("\t") == [
        "status", "timestamp", "step", "label", "actual", "expected", "source",
    ]
    fields = rows[1].split("\t")
    assert fields[0] == "PASS"
    assert fields[2] == "test"
    assert fields[3] == "transcripts"
    assert fields[6] == "GENCODE v44"


def test_summary_tally(log):
    check("a", 1, 1)
    check("b", 2, 3, warn_only=True)
    assert summary() == {"pass": 1, "fail": 1}
    assert "2 checks: 1 passed, 1 failed" in open(log + ".log").read()


def test_init_truncates_previous_log(tmp_path):
    prefix = str(tmp_path / "checks")
    init(prefix, step="first")
    check("a", 1, 1)
    init(prefix, step="second")
    assert "first" not in open(prefix + ".log").read()
    assert len(open(prefix + ".tsv").read().strip().split("\n")) == 1
