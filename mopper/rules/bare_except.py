"""Rule: flags a bare except clause that catches every exception type."""
import ast
from mopper.linter import Rule


class BareExcept(Rule):
    code = "B002"
    message = "bare 'except:' clause — catch a specific exception instead"

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.add(node)
        self.generic_visit(node)
