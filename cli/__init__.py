import curses as cr

from cli.style import StyledLine
from cli.color import init_colors

console = cr.initscr()
cr.noecho()
cr.cbreak()
cr.curs_set(True)
cr.mousemask(-1)

console.keypad(True)


def initialize():
    init_colors()


def show_line(line: StyledLine, offset: int, width: int):
    assert offset >= 0 and width >= 0
    left, right = offset, offset + width
    for cmp in line.contents:
        if left in range(len(cmp.content)):
            data = cmp.content[left:right]
        elif right in range(len(cmp.content)):
            data = cmp.content[:right]
        else:
            continue

        color_attr = cr.color_pair(
            cmp.style.select_color if line.is_selected else cmp.style.basic_color
        )
        console.addstr(data, color_attr)
