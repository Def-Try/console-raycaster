import curses

import drawing
import utils
import world


def main(screen):
    nextlevel = 'maps/level0.txt'
    draw = drawing.Drawing(screen, {'#': ['amogus?!?!?', 'RRRRRRWWWWW'], '?': [" ", "W"]})
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    for i in range(1, 256):
        curses.init_pair(i, i, curses.COLOR_BLACK)
    while True:
        worldmap = world.World(nextlevel)
        utils.playerpos = utils.Vec2(2, 2)
        while True:
            draw.renderworld(worldmap, utils.playerpos, utils.playerangle)
            draw.rendermap(worldmap, utils.playerpos)
            draw.debuginfo(round(utils.playerpos, 2), round(utils.playerangle, 2))
            draw.flush()

            x = utils.handlecontrols(screen, worldmap)
            if x == 'NEXT':
                nextlevel = 'maps/' + worldmap.get_next()
                break


curses.wrapper(main)

# update
