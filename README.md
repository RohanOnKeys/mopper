# mopper

A lightweight Python linter built on the standard library's `ast` module, with **zero runtime dependencies**.

`mopper` doesn't aim to replace tools like Flake8 or Pylint. Instead, it focuses on a small set of practical checks that catch common mistakes such as unused imports, mutable default arguments, bare `except` clauses, unreachable code, and more.

## Installation

```bash
pip install mopper
```

## Usage

```bash
mopper path/to/file.py
mopper path/to/project/
mopper . --select B001,B003
mopper . --format json
```

## Rules

| Code | Check |
|------|-------|
| B001 | Unused import |
| B002 | Bare `except` clause |
| B003 | Mutable default argument |
| B004 | Comparing to `None`, `True`, or `False` with `==` instead of `is` |
| B005 | Unreachable code after `return`, `raise`, `break`, or `continue` |
| B006 | Line longer than 100 characters |

## Why mopper?

`mopper` was built from scratch to understand how Python static analysis works internally using only the standard library. It demonstrates how a practical linter can be implemented with `ast.NodeVisitor` and a simple, extensible rule system.

## License

MIT
