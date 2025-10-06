from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


class GSet[T]:
    """
    A Grow-only Set (G-Set) CRDT.

    This set only allows additions; elements cannot be removed.
    It is useful for scenarios where elements are only ever added,
    and conflicts are resolved by taking the union of all elements.

    Agricultural Context:
    Used for tracking immutable facts, suchs as a set of completed tasks
    (e.g., harvested field sections, applied treatments) where once an
    item is added, it remains part of the set.
    """

    def __init__(self) -> None:
        self._elements: set[T] = set()

    def add(self, element: T) -> None:
        """Adds an element to the set."""
        self._elements.add(element)

    def merge(self, other: GSet[T]) -> None:
        """Merges this G-Set with another G-Set."""
        self._elements.update(other._elements)

    def __contains__(self, element: T) -> bool:
        """Checks if an element is in the set."""
        return element in self._elements

    def __len__(self) -> int:
        """Returns the number of elements in the set."""
        return len(self._elements)

    def __repr__(self) -> str:
        return f"GSet({self._elements})"

    def get_state(self) -> set[T]:
        """Returns the current state (elements) of the G-Set."""
        return self._elements
