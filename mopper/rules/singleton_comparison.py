"""Rule: flags == or != comparisons against None, True, or False."""
import ast
from mopper.linter import Rule


class SingletonComparison(Rule):
    code = "B004"
    message = "use 'is' / 'is not' when comparing to None, True, or False"

    def visit_Compare(self, node: ast.Compare):
        operands = [node.left] + node.comparators
        for op in node.ops:
            if isinstance(op, (ast.Eq, ast.NotEq)):
                for operand in operands:
                    if isinstance(operand, ast.Constant) and operand.value in (None, True, False):
                        self.add(node)
                        break
        self.generic_visit(node)
