from dataclasses import dataclass
from typing import Optional

type JTypes = None | bool | float | str | list | dict | tuple


@dataclass
class Item:
    value: JTypes
    level: int
    name: str = "unnamed"
    collapse: list["Item"] | None = None
    parent: Optional["Item"] = None
    close: Optional["Item"] = None

    def __repr__(self):
        pr = id(self.parent) if self.parent else None
        cl = id(self.close) if self.close else None
        return (
            f"Item(id={id(self)}, level={self.level}, name={self.name}, "
            f"value={repr(self.value)}, collapse={bool(self.collapse)}, parent={pr}, "
            f"close={cl})"
        )


def new_none(level: int) -> Item:
    return Item(value=None, level=level)


def new_primitive(value: bool | float | str, level: int) -> Item:
    return Item(value=value, level=level)


def new_list(level: int) -> Item:
    return Item(value=[], level=level)


def new_dict(level: int) -> Item:
    return Item(value={}, level=level)


def new_close(parent: Item, level: int) -> Item:
    close_item = Item(value=(), level=level, parent=parent)
    parent.close = close_item
    return close_item
