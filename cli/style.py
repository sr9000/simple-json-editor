from dataclasses import dataclass
from cli.color import (
    C_NONE,
    C_TEXT,
    C_WHITE,
    C_RED,
    C_GREEN,
    C_BLUE,
    C_YELLOW,
    C_CYAN,
    C_PURPLE,
    C_INVERT,
    C_DISABLED,
    C_SHIFT,
)


@dataclass
class Style:
    basic_color: int
    select_color: int


@dataclass
class Content:
    content: str
    style: Style


@dataclass
class StyledLine:
    contents: list[Content]
    is_selected: bool


S_DEFAULT = Style(C_TEXT, C_WHITE + C_INVERT)
S_DARK = Style(C_DISABLED, C_WHITE + C_INVERT)
S_DISABLED = Style(C_DISABLED, C_DISABLED + C_INVERT)
S_ERROR = Style(C_RED + C_INVERT, C_RED + C_INVERT + C_SHIFT)
S_WARNING = Style(C_YELLOW + C_INVERT, C_YELLOW + C_INVERT + C_SHIFT)
S_INFO = Style(C_WHITE + C_INVERT, C_WHITE + C_INVERT)
S_KIND = Style(C_CYAN, C_CYAN + C_INVERT)

S_STRING = Style(C_GREEN + C_SHIFT, C_GREEN + C_SHIFT + C_INVERT)
S_NUMBER = Style(C_BLUE + C_SHIFT, C_BLUE + C_SHIFT + C_INVERT)
S_NULL = Style(C_PURPLE + C_SHIFT, C_PURPLE + C_SHIFT + C_INVERT)
S_BOOL = Style(C_YELLOW, C_YELLOW + C_INVERT)
S_NONE = Style(C_NONE, C_WHITE + C_INVERT)
