import json

from utils import Vec2, tolist, tostr


class World:
    def __init__(self, level='maps/level0.txt'):
        self.name = ''
        level = self.load(level)
        self.levelmap, self.levellight, self.map_width, self.map_height = self.make_map(level['terrain'], level['lighting'])
        self.levellight = self.calc_light(self.levellight)

    def calc_light(self, lightmap):
        newmap = tolist(lightmap)
        for x in range(self.map_width):
            for y in range(self.map_height):
                if self.get_light(Vec2(x, y)) == '#':
                    for tx in range(x-1,x+1):
                        for ty in range(y-1,y+1):
                            if self.get_light(Vec2(tx, ty)) != '#':
                                newmap[y * self.map_width + x] = '.'
        return tostr(newmap)

    @staticmethod
    def make_map(string_map, string_light):
        rows = string_map.strip().split('\n')
        h = len(rows)
        w = len(rows[0])
        return string_map.replace('\n', ''), string_light.replace('\n', ''), w, h

    @staticmethod
    def load(file):
        lfile = open(file, 'r')
        level = json.loads(lfile.read())
        lfile.close()
        return level

    def get_block(self, pos: Vec2):
        pos = round(pos)
        if 0 <= pos.x < self.map_width and 0 <= pos.y < self.map_height:
            return self.levelmap[pos.y * self.map_width + pos.x]
        return '?'

    def get_light(self, pos: Vec2):
        pos = round(pos)
        if 0 <= pos.x < self.map_width and 0 <= pos.y < self.map_height:
            return self.levellight[pos.y * self.map_width + pos.x]
        return ' '
