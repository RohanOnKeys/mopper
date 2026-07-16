"""Public API for mopper: exposes Linter, Rule, and Violation for library use."""
from mopper.linter import Linter, Rule, Violation

__version__ = "0.1.1"
__all__ = ["Linter", "Rule", "Violation"]
