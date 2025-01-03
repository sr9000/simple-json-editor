import curses as cr


def init_colors():
    cr.start_color()
    cr.use_default_colors()

    assert cr.COLORS >= 16, f"{cr.COLORS=}"

    for i in range(0, 16):
        cr.init_pair(i, i, -1)
        cr.init_pair(i + 16, -1, i)


C_SHIFT = 8
C_INVERT = 16

C_TEXT = 0
C_DISABLED = C_TEXT + C_SHIFT
C_NONE = C_TEXT + C_INVERT

C_RED = 1
C_GREEN = 2
C_YELLOW = 3
C_BLUE = 4
C_PURPLE = 5
C_CYAN = 6
C_WHITE = 7
