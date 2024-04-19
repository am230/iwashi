from typing import Iterable


def iterable_eq(a: Iterable, b: Iterable) -> bool:
    # Compare two iterables for equality
    # ignoring the order of elements
    for item in a:
        if item not in b:
            return False
    for item in b:
        if item not in a:
            return False
    return True
