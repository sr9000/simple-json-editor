from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar


# NAF no args func
NAF = TypeVar("NAF", bound=Callable[[], None])


class AbstractChanges(ABC):
    @abstractmethod
    def apply(self): ...
    @abstractmethod
    def rollback(self): ...
    @property
    @abstractmethod
    def reversed(self) -> "AbstractChanges": ...


@dataclass(frozen=True)
class Changes(AbstractChanges):
    apply_func: NAF
    rollback_func: NAF

    def apply(self):
        self.apply_func()

    def rollback(self):
        self.rollback_func()

    @property
    def reversed(self) -> "Changes":
        return Changes(self.rollback_func, self.apply_func)


@dataclass(frozen=True)
class MultiChanges(AbstractChanges):
    seq: tuple[AbstractChanges, ...]

    def apply(self):
        for ch in self.seq:
            ch.apply()

    def rollback(self):
        for ch in reversed(self.seq):
            ch.rollback()

    @property
    def reversed(self) -> "MultiChanges":
        return MultiChanges(tuple(ch.reversed for ch in self.seq[::-1]))


ZERO_CHANGES = Changes(lambda: None, lambda: None)


class History:
    def __init__(self, limit=1000):
        self.limit = max(10, limit)
        self.dropout = self.limit // 3
        self.commits: list[AbstractChanges] = [ZERO_CHANGES]
        self.ptr = 0

    @property
    def has_redo(self) -> bool:
        return self.ptr + 1 != len(self.commits)

    @property
    def has_undo(self) -> bool:
        return self.ptr != 0

    def redo(self):
        if self.has_redo:
            self.ptr += 1
            self.commits[self.ptr].apply()

    def undo(self):
        if self.has_undo:
            self.commits[self.ptr].rollback()
            self.ptr -= 1

    def commit(self, ch: AbstractChanges) -> None:
        if self.has_redo:
            tail = MultiChanges(tuple(self.commits[self.ptr + 1:]))
            self.commits.append(tail.reversed)
            self.ptr = len(self.commits) - 1

        ch.apply()
        self.commits.append(ch)
        self.ptr += 1

        if self.ptr > self.limit:
            self.commits = self.commits[self.dropout:]
            self.ptr = len(self.commits) - 1
