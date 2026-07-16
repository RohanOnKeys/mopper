"""Rule: flags an import whose name never appears anywhere else in the file."""
import ast
from mopper.linter import Rule


class UnusedImport(Rule):
    code = "B001"
    message = "imported but unused"

    def visit_Module(self, node: ast.Module):
        imported: dict[str, ast.AST] = {}
        used: set[str] = set()

        for n in ast.walk(node):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                for alias in n.names:
                    name = alias.asname or alias.name.split(".")[0]
                    if name != "*":
                        imported[name] = n
            elif isinstance(n, ast.Name):
                used.add(n.id)
            elif isinstance(n, ast.Attribute):
                # handles `os.path` style usage where only `os` shows as a Name
                pass

        for name, import_node in imported.items():
            if name not in used:
                self.add(import_node, f"'{name}' {self.message}")
