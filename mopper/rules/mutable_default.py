"""Rule: flags mutable default arguments such as def f(x=[])."""
import ast
from mopper.linter import Rule

MUTABLE_TYPES = (ast.List, ast.Dict, ast.Set)


class MutableDefault(Rule):
    code = "B003"
    message = "mutable default argument — use None and set the default inside the function"

    def _check(self, node):
        defaults = list(node.args.defaults) + list(node.args.kw_defaults)
        for d in defaults:
            if isinstance(d, MUTABLE_TYPES):
                self.add(d)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._check(node)
        self.generic_visit(node)
