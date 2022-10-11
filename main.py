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
        player = utils.Player(worldmap.get_start(), utils.Vec2(0, 0))
        while True:
            draw.renderworld(worldmap, player)
            draw.rendermap(worldmap, player)
            draw.debuginfo(round(player.pos, 2), round(player.ang, 2))
            draw.flush()

            x = player.handlecontrols(screen, worldmap)
            if x == 'NEXT':
                nextlevel = 'maps/' + worldmap.get_next()
                break


curses.wrapper(main)

# update
