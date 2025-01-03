from model.item import *
from collections import deque

type Allowed = None | bool | float | int | str | list | tuple | dict


def from_value(value: Allowed, level: int = 0) -> list[Item]:
    res: list[Item] = []

    match value:
        case None:
            res.append(new_none(level))
        case bool(x) | float(x) | str(x):
            res.append(new_primitive(x, level))
        case int(x):
            res.append(new_primitive(float(x), level))
        case list(xs) | tuple(xs):
            parent = new_list(level)
            res.append(parent)
            for i, x in enumerate(xs):
                sub_res = from_value(x, level + 1)
                sub_res[0].parent = parent
                sub_res[0].alias = i
                res.extend(sub_res)
            res.append(new_close(parent, level + 1))
        case dict(kvs):
            parent = new_dict(level)
            res.append(parent)
            for k, v in kvs.items():
                sub_res = from_value(v, level + 1)
                sub_res[0].parent = parent
                sub_res[0].alias = k
                res.extend(sub_res)
            res.append(new_close(parent, level + 1))
        case _:
            raise TypeError(f"unconvertable type: {type(value)}")

    return res


def to_value(items: list[Item]) -> Allowed:
    rest = deque(items)
    stack = [[]]

    def put(col: list | dict, val: JTypes, name: str):
        match col:
            case list(lst):
                lst.append(val)
            case dict(dct):
                dct[name] = val
            case _:
                raise TypeError(f"not supported collection type: {type(col)}")

    while rest:
        it = rest.popleft()
        match it.value:
            case None:
                put(stack[-1], None, it.alias)
            case bool(x) | float(x) | str(x):
                put(stack[-1], x, it.alias)
            case list(_):
                xs = []
                put(stack[-1], xs, it.alias)
                stack.append(xs)
                if it.collapsed:
                    rest.extendleft(it.collapsed)
            case dict(_):
                kvs = {}
                put(stack[-1], kvs, it.alias)
                stack.append(kvs)
                if it.collapsed:
                    rest.extendleft(it.collapsed)
            case tuple(_):
                if len(stack) == 1:
                    raise IndexError("there is no collection to be closed on stack")
                stack.pop()
            case _:
                raise TypeError(f"not supported item value type: {type(it.value)}")

    assert len(stack) > 0, "stack cannot be empty"

    if len(stack) > 1:
        raise ValueError(f"too many ({len(stack)}) values left on stack ")

    res = stack.pop()

    assert len(res) > 0, "result cannot be empty"

    if len(res) > 1:
        raise ValueError(f"too many ({len(res)}) values got after conversion")

    return res.pop()
