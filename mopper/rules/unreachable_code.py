"""Rule: flags statements that can never execute after a return, raise, continue, or break."""
import ast
from mopper.linter import Rule


class UnreachableCode(Rule):
    code = "B005"
    message = "unreachable code after return/raise/continue/break"

    def _check_body(self, body: list[ast.stmt]):
        terminators = (ast.Return, ast.Raise, ast.Continue, ast.Break)
        for i, stmt in enumerate(body):
            if isinstance(stmt, terminators) and i + 1 < len(body):
                self.add(body[i + 1])
                break

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._check_body(node.body)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._check_body(node.body)
        self.generic_visit(node)
