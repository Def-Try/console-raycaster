import curses

import drawing
import utils
import world


def main(screen):
    worldmap = world.World()
    draw = drawing.Drawing(screen, {'#': ['amogus?!?!?', 'RRRRRRWWWWW'], '?': ["", ""]})
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    for i in range(1, 256):
        curses.init_pair(i, i, curses.COLOR_BLACK)
    while True:
        draw.renderworld(worldmap, utils.playerpos, utils.playerangle)
        draw.rendermap(worldmap, utils.playerpos)
        draw.debuginfo(round(utils.playerpos, 2), round(utils.playerangle, 2))
        draw.flush()

        utils.handlecontrols(screen, worldmap)


curses.wrapper(main)
