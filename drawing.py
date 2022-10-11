import curses
from math import cos, radians
from time import time

from raycasting import Raycasting
from utils import Vec2
from world import World

FOV = radians(90)
DEPTH = 16
TILESIZE = 10

colors = {
    'R': (88, 124, 160),
    'B': (17, 19, 21),
    'G': (22, 2, 40),
    'C': (26, 9, 39),
    'M': (5, 13, 127),
    'Y': (6, 220, 226),
    'W': (7, 8, 15)
}


class Drawing:
    def __init__(self, screen, textures):
        self.screen = screen
        self.caster = Raycasting()
        self.textures = textures
        self.frame = 0
        self.oframe = 0
        self.fps = "..."
        self.time = time()

    def get_texture(self, b, c, r):
        if b == "?":
            return " ", 0
        if b == 'E':
            return "THE END IS NEVER "[(r * TILESIZE + c + self.frame % 17) % 17], self.frame % 255
        try:
            blocktexture = self.textures[b]
            return blocktexture[0][(r * TILESIZE + c) % len(blocktexture[0])], \
                   colors[blocktexture[1][(r * TILESIZE + c) % len(blocktexture[1])]]
        except KeyError:
            return "b", colors['W']

    def flush(self):
        self.screen.refresh()

    def debuginfo(self, playerpos, playerangle):
        if (time() - self.time) > 1:
            self.fps = round((self.frame - self.oframe) / (time() - self.time))
            self.time = time()
            self.oframe = self.frame
        h, w = self.screen.getmaxyx()
        self.screen.addstr(h - 1, 0, "Pos: " + str(playerpos) + "  Ang: " + str(playerangle))
        self.screen.addstr(0, w - len("FPS:" + str(self.fps)), "FPS:" + str(self.fps))

    def rendermap(self, world: World, player):
        for col in range(10):
            for row in range(10):
                if not (row == int(world.map_width / 2) and col == int(world.map_height / 2)):
                    mblock = world.get_block(Vec2(round(player.pos.x + row - world.map_width / 2),
                                                  round(player.pos.y + col - world.map_height / 2)))
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

    def renderworld(self, world: World, player):
        self.frame += 1
        screen_height, screen_width = self.screen.getmaxyx()
        player_light = world.get_light(player.pos)
        for col in range(screen_width):
            rayangle = (player.ang.x - FOV / 2) + (col / screen_width) * FOV
            block, light, dist = self.caster.raycast(player.pos, rayangle, 8, 0.1, world)
            dist *= cos(player.ang.x - rayangle)
            if block not in (' ', '.'):
                ceiling = int(screen_height / 2 - screen_height / dist) + player.ang.y
                floor = int(screen_height - ceiling + player.ang.y * 2)

                for row in range(screen_height):
                    if row <= ceiling:
                        tex = "█"
                        color = curses.COLOR_CYAN
                        shade = curses.A_BOLD
                    elif floor >= row > ceiling:
                        tex, color = self.get_texture(block, col, row)
                        if player_light == '.':
                            dist /= 4
                        elif player_light == ' ':
                            dist /= 2
                        if dist <= DEPTH / 3:
                            shade = curses.A_BOLD
                        elif dist <= DEPTH / 2:
                            shade = curses.A_NORMAL
                        elif dist <= DEPTH:
                            shade = curses.A_DIM
                        else:
                            tex = " "
                            shade = curses.A_DIM
                        if block == '?':
                            tex = ""
                    else:
                        color = curses.COLOR_BLUE
                        tex = "█"
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
                    if player_light == '.':
                        if shade == curses.A_BOLD:
                            shade = curses.A_NORMAL
                        else:
                            shade = curses.A_DIM
                    elif player_light == ' ':
                        shade = curses.A_DIM
                    if player_light == '.':
                        if 0 <= row < 1:
                            tex = " "
                        elif 0 <= col < 2:
                            tex = " "
                        elif screen_height - 1 <= row < screen_height:
                            tex = " "
                        elif screen_width - 2 <= col < screen_width:
                            tex = " "
                    elif player_light == ' ':
                        if 0 <= row < 2:
                            tex = " "
                        elif 0 <= col < 3:
                            tex = " "
                        elif screen_height - 2 <= row < screen_height:
                            tex = " "
                        elif screen_width - 3 <= col < screen_width:
                            tex = " "

                    if type(color) is tuple:
                        if shade == curses.A_BOLD:
                            color = color[2]
                        elif shade == curses.A_NORMAL:
                            color = color[1]
                        elif shade == curses.A_DIM:
                            color = color[0]
                    self.screen.insstr(row, col, tex, curses.color_pair(color) | shade)

# update
