from math import cos, sin, radians

from utils import Vec2

TILESIZE = 10
FOV = radians(90)


class Raycasting:
    @staticmethod
    def raycast(origin, angle, maxdist, step, world):
        distance = 0.0
        direction = Vec2(sin(angle), cos(angle))
        while distance < maxdist:
            distance += step
            test_vec = origin + direction * distance
            if test_vec == origin:
                continue
            block = world.get_block(test_vec)
            light = world.get_light(test_vec)
            if block not in (' ', '?', '.', 'S'):
                return block, light, distance
        return '?', '.', maxdist - 0.01
