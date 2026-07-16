"""Test suite: one check per rule, plus a control case that should stay clean."""
from pathlib import Path

from mopper.linter import Linter
from mopper.rules import ALL_RULES, RULES_BY_CODE

FIXTURE = Path(__file__).parent / "fixtures" / "broken.py"


def codes_found():
    linter = Linter(ALL_RULES)
    violations = linter.lint_file(str(FIXTURE))
    return {v.code for v in violations}


def test_unused_import_detected():
    assert "B001" in codes_found()


def test_bare_except_detected():
    assert "B002" in codes_found()


def test_mutable_default_detected():
    assert "B003" in codes_found()


def test_singleton_comparison_detected():
    assert "B004" in codes_found()


def test_unreachable_code_detected():
    assert "B005" in codes_found()


def test_clean_file_has_no_violations(tmp_path):
    clean = tmp_path / "clean.py"
    clean.write_text("def add(a, b):\n    return a + b\n")
    linter = Linter(ALL_RULES)
    assert linter.lint_file(str(clean)) == []
