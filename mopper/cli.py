"""Command line interface: argument parsing, file collection, output formatting."""
import argparse
import json
import sys
from pathlib import Path

from mopper.linter import Linter, Violation
from mopper.rules import ALL_RULES, RULES_BY_CODE

MAX_LINE_LENGTH = 100


def check_line_length(source: str, limit: int = MAX_LINE_LENGTH) -> list[Violation]:
    violations = []
    for i, line in enumerate(source.splitlines(), start=1):
        if len(line) > limit:
            violations.append(
                Violation(line=i, col=limit, code="B006", message=f"line too long ({len(line)} > {limit})")
            )
    return violations


def collect_files(target: str) -> list[Path]:
    path = Path(target)
    if path.is_file():
        return [path]
    return sorted(path.rglob("*.py"))


def format_text(path: Path, violations: list[Violation]) -> str:
    return "\n".join(f"{path}:{v.line}:{v.col}: {v.code} {v.message}" for v in violations)


def format_json(results: dict[str, list[Violation]]) -> str:
    payload = {
        str(path): [{"line": v.line, "col": v.col, "code": v.code, "message": v.message} for v in vs]
        for path, vs in results.items()
    }
    return json.dumps(payload, indent=2)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="mopper", description="A small, fast, AST-based Python linter.")
    parser.add_argument("target", help="file or directory to lint")
    parser.add_argument("--select", help="comma-separated rule codes to run, e.g. B001,B002")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    if args.select:
        codes = {c.strip() for c in args.select.split(",")}
        rules = [r for r in ALL_RULES if r.code in codes]
    else:
        rules = ALL_RULES

    linter = Linter(rules)
    files = collect_files(args.target)
    results: dict[Path, list[Violation]] = {}
    total = 0

    for path in files:
        source = path.read_text(encoding="utf-8")
        try:
            violations = linter.lint_source(source, filename=str(path))
        except SyntaxError as e:
            violations = [Violation(line=e.lineno or 0, col=e.offset or 0, code="B000", message=f"syntax error: {e.msg}")]
        if not args.select or "B006" in (args.select or "B006"):
            violations += check_line_length(source)
        violations.sort(key=lambda v: (v.line, v.col))
        if violations:
            results[path] = violations
            total += len(violations)

    if args.format == "json":
        print(format_json(results))
    else:
        for path, violations in results.items():
            print(format_text(path, violations))
        if total:
            print(f"\n{total} violation(s) found in {len(results)} file(s).")
        else:
            print("mopper: no issues found 🌱")

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
