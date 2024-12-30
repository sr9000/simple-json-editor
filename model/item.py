from dataclasses import dataclass

type JClose = tuple
type JTypes = None | bool | float | str | list | dict | JClose


@dataclass
class Item:
    value: JTypes
    level: int
    name: str = "unnamed"
    collapse: list['Item'] | None = None
    parent: 'Item' | None = None
    close: 'Item' | None = None


def wrap_none(level: int) -> Item:
    return Item(value=None, level=level)


def wrap_primitive(value: bool | float | str, level: int) -> Item:
    return Item(value=value, level=level)


def wrap_list(level: int) -> Item:
    return Item(value=[], level=level)


def wrap_dict(level: int) -> Item:
    return Item(value={}, level=level)


def wrap_close(parent: Item, level: int) -> Item:
    close_item = Item(value=(), level=level, parent=parent)
    parent.close = close_item
    return close_item
