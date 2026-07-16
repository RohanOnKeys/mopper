"""Fixture file: contains one deliberate violation for each rule mopper checks."""
import os  # unused import -> B001
import sys

print(sys.version)


def bad_default(items=[]):  # mutable default -> B003
    items.append(1)
    return items


def check(x):
    if x == None:  # singleton comparison -> B004
        return True
    return False


try:
    1 / 0
except:  # bare except -> B002
    pass


def unreachable():
    return 1
    print("never runs")  # unreachable -> B005
