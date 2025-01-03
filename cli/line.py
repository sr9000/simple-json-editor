from dataclasses import dataclass, field

from cli.style import (
    StyledLine,
    Content,
    S_KIND,
    S_BOOL,
    S_NUMBER,
    S_STRING,
    S_DEFAULT,
    S_NULL,
    S_DARK,
    S_DISABLED,
)
from model.item import JTypes, TAlias


@dataclass
class ValueStatus:
    is_collapsed: bool
    is_selected: bool
    is_enabled: bool


@dataclass
class LineConfig:
    tab_size: int = field(default=4)
    show_types: bool = field(default=True)


TEXT_IS_COLLAPSED = {
    True: "+",
    False: "-",
}

TEXT_VALUE_TYPE = {
    type(None): "-",
    bool: "bool",
    float: "number",
    str: "string",
    list: "array",
    dict: "object",
    tuple: "",  # closing value
}


STYLE_VALUE_TYPE = {
    type(None): S_NULL,
    bool: S_BOOL,
    float: S_NUMBER,
    str: S_STRING,
    list: S_DEFAULT,
    dict: S_DEFAULT,
    tuple: S_DEFAULT,  # closing value
}


def make_styled_line(
    alias: TAlias,
    value: JTypes,
    level: int,
    status: ValueStatus,
    conf: LineConfig = LineConfig(),
) -> StyledLine:
    components = []
    feed = Content(" ", S_DEFAULT if status.is_enabled else S_DISABLED)

    deep = ("." + " " * (conf.tab_size - 1)) * level
    match value:
        case tuple(_):
            deep += "."
        case list(_) | dict(_):
            deep += TEXT_IS_COLLAPSED[status.is_collapsed]
        case _:
            deep += " "

    components.append(Content(deep, S_DARK if status.is_enabled else S_DISABLED))
    components.append(feed)

    match alias:
        case None:
            pass
        case int(index):
            components.append(
                Content(f"[{index}]", S_DARK if status.is_enabled else S_DISABLED)
            )
            components.append(feed)
        case str(name):
            components.append(
                Content(name, S_DEFAULT if status.is_enabled else S_DISABLED)
            )
            components.append(feed)
        case _:
            raise TypeError(f"not supported alias type: {type(alias)}")

    if conf.show_types or isinstance(value, list | dict):
        components.append(
            Content(
                TEXT_VALUE_TYPE[type(value)],
                S_KIND if status.is_enabled else S_DISABLED,
            )
        )
        components.append(feed)

    components.append(
        Content(
            repr(value),
            STYLE_VALUE_TYPE[type(value)] if status.is_enabled else S_DISABLED,
        )
    )
    components.append(feed)

    return StyledLine(components, status.is_selected)
