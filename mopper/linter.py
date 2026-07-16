"""Core engine: walks a file's AST and runs every registered rule against it."""
import ast
from dataclasses import dataclass


@dataclass
class Violation:
    line: int
    col: int
    code: str
    message: str


class Rule(ast.NodeVisitor):
    """Base class for every check. Subclass and override the relevant visit_* method."""
    code: str = "B000"
    message: str = "unspecified violation"

    def __init__(self):
        self.violations: list[Violation] = []

    def add(self, node: ast.AST, message: str | None = None):
        self.violations.append(
            Violation(
                line=node.lineno,
                col=node.col_offset,
                code=self.code,
                message=message or self.message,
            )
        )


class Linter:
    def __init__(self, rules: list[type[Rule]]):
        self.rules = rules

    def lint_source(self, source: str, filename: str = "<string>") -> list[Violation]:
        tree = ast.parse(source, filename=filename)
        violations: list[Violation] = []
        for rule_cls in self.rules:
            rule = rule_cls()
            rule.visit(tree)
            violations.extend(rule.violations)
        # line-based rules (not AST) get bolted on separately in cli.py
        return sorted(violations, key=lambda v: (v.line, v.col))

    def lint_file(self, path: str) -> list[Violation]:
        with open(path, encoding="utf-8") as f:
            source = f.read()
        return self.lint_source(source, filename=path)
