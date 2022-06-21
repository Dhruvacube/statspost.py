from typing import Any


class _MissingSentinel:
    """A type safe sentinel for the `None` type.
    """    
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return "..."

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


MISSING: Any = _MissingSentinel()
