"""Central registry of every active rule mopper runs against a file."""
from mopper.rules.unused_import import UnusedImport
from mopper.rules.bare_except import BareExcept
from mopper.rules.mutable_default import MutableDefault
from mopper.rules.singleton_comparison import SingletonComparison
from mopper.rules.unreachable_code import UnreachableCode

ALL_RULES = [
    UnusedImport,
    BareExcept,
    MutableDefault,
    SingletonComparison,
    UnreachableCode,
]

RULES_BY_CODE = {rule.code: rule for rule in ALL_RULES}
