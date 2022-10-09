import curses
import json
import os

import drawing
import utils
import world


def make_textures():
    def parse_texture(file):
        lfile = open(file, 'r', encoding='utf-8')
        texture = json.loads(lfile.read())
        lfile.close()
        return [texture['texture'], texture['clrmask']]

    textures = {}
    for file in os.listdir(os.fsencode("textures")):
        filename = os.fsdecode(file)
        texturename = filename.split('.')[0]
        ttex = parse_texture("textures/" + filename)
        textures[texturename] = ttex
    return textures


def main(screen):
    nextlevel = 'maps/level0.txt'
    draw = drawing.Drawing(screen, make_textures())
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
