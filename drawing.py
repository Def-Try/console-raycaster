import curses
from math import cos, radians

from raycasting import Raycasting
from utils import Vec2
from world import World

FOV = radians(90)
DEPTH = 16
TILESIZE = 40

colors = {
    'RED': curses.COLOR_RED,
    'WHITE': curses.COLOR_WHITE,
    'YELLOW': curses.COLOR_YELLOW,
    'BLUE': curses.COLOR_BLUE,
    'GREEN': curses.COLOR_GREEN,
    'CYAN': curses.COLOR_CYAN,
    'MAGENTA': curses.COLOR_MAGENTA,
    'R': curses.COLOR_RED,
    'W': curses.COLOR_WHITE,
    'Y': curses.COLOR_YELLOW,
    'B': curses.COLOR_BLUE,
    'G': curses.COLOR_GREEN,
    'C': curses.COLOR_CYAN,
    'M': curses.COLOR_MAGENTA
}

class Drawing:
    def __init__(self, screen, textures):
        self.screen = screen
        self.caster = Raycasting()
        self.textures = textures
        self.frame = 0

    def get_texture(self, b, c, r):
        if b == 'E':
            return "THE END IS NEVER "[(r * TILESIZE + c + self.frame % 17) % 17], self.frame % 255
        try:
            blocktexture = self.textures[b]
            return blocktexture[0][(r * TILESIZE + c) % len(blocktexture[0])], \
                   colors[blocktexture[1][(r * TILESIZE + c) % len(blocktexture[1])]]
        except KeyError:
            return "b", curses.COLOR_WHITE

    def flush(self):
        self.screen.refresh()

    def debuginfo(self, playerpos, playerangle):
        h, w = self.screen.getmaxyx()
        self.screen.addstr(h-1,0, "Pos: " + str(playerpos) + "  Ang: " + str(playerangle))

    def rendermap(self, world: World, playerpos):
        for col in range(10):
            for row in range(10):
                if not (row == int(world.map_width / 2) and col == int(world.map_height / 2)):
                    mblock = world.get_block(Vec2(round(playerpos.x + row - world.map_width / 2),
                                             round(playerpos.y + col - world.map_height / 2)))
                    tex = mblock
                    if mblock == "?":
                        tex = " "
                    color = curses.COLOR_WHITE
                    shade = curses.A_DIM
                else:
                    tex = "P"
                    color = curses.COLOR_RED
                    shade = curses.A_BOLD
                self.screen.addstr(row, col, tex, curses.color_pair(color) | shade)

    def renderworld(self, world: World, playerpos, playerangle):
        prevtex = " "
        self.frame += 1
        screen_height, screen_width = self.screen.getmaxyx()
        player_light = world.get_light(playerpos)
        for col in range(screen_width):
            rayangle = (playerangle.x - FOV / 2) + (col / screen_width) * FOV
            block, light, dist = self.caster.raycast(playerpos, rayangle, 32, 0.1, world)
            dist *= cos(playerangle.x - rayangle)
            if block not in (' ', '.'):
                ceiling = int(screen_height / 2 - screen_height / dist) + playerangle.y
                floor = int(screen_height - ceiling + playerangle.y * 2)

                for row in range(screen_height):
                    if row <= ceiling:
                        tex = "C"
                        color = curses.COLOR_CYAN
                        shade = curses.A_BOLD
                    elif floor >= row > ceiling:
                        tex, color = self.get_texture(block, col, row)
                        if dist <= DEPTH / 3:
                            shade = curses.A_BOLD
                        elif dist <= DEPTH / 2:
                            shade = curses.A_NORMAL
                        elif dist <= DEPTH:
                            shade = curses.A_DIM
                        else:
                            tex = " "
                            shade = curses.A_DIM

                        if block == "?":
                            tex = prevtex
                            dist = 0
                            shade = curses.A_NORMAL
                            color = curses.COLOR_BLACK
                    else:
                        color = curses.COLOR_BLUE
                        tex = "F"
                        shade = curses.A_BOLD
                    if light == '.':
                        if shade == curses.A_BOLD:
                            shade = curses.A_NORMAL
                        elif shade == curses.A_NORMAL:
                            shade = curses.A_DIM
                        elif shade == curses.A_DIM:
                            shade = curses.A_NORMAL
                            tex = " "
                    if light == ' ':
                        if shade == curses.A_BOLD:
                            shade = curses.A_DIM
                        elif shade == curses.A_NORMAL:
                            shade = curses.A_NORMAL
                            tex = " "
                        elif shade == curses.A_DIM:
                            shade = curses.A_NORMAL
                            tex = " "
                    if 0 <= row < 2:
                        if 0 <= col < 2:
                            tex = " "
                    self.screen.insstr(row, col, tex, curses.color_pair(color) | shade)
                    prevtex = tex

# update
