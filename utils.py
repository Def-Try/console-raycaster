from math import cos, sin, degrees, radians

SPEED = 0.3
ROTATION_SPEED = radians(5)

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __get__(self, instance, owner):
        return instance

    def __round__(self, f=0):
        if f != 0:
            return Vec2(round(self.x, f), round(self.y, f))
        return Vec2(round(self.x), round(self.y))

    def __add__(self, other):
        if type(other) == Vec2:
            return Vec2(self.x + other.x, self.y + other.y)
        elif type(other) == int or type(other) == float:
            return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other) == Vec2:
            return Vec2(self.x - other.x, self.y - other.y)
        elif type(other) == int or type(other) == float:
            return Vec2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vec2:
            return Vec2(self.x * other.x, self.y * other.y)
        elif type(other) == int or type(other) == float:
            return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) == Vec2:
            return Vec2(self.x / other.x, self.y / other.y)
        elif type(other) == int or type(other) == float:
            return Vec2(self.x / other, self.y / other)

    def __str__(self):
        return f"Vec2{self.x, self.y}"

def tolist(istr):
    glist = {}
    for i in range(len(istr)):
        glist[i] = istr[i]
    return glist

def tostr(ilist):
    gstr = ""
    for i in range(len(ilist)):
        gstr += ilist[i]
    return gstr

playerpos = Vec2(2,2)
playerangle = Vec2(0,0)

def handlecontrols(screen, world):
    global playerpos, playerangle
    screen.timeout(1)
    key_code = screen.getch()
    key = chr(key_code) if 0 < key_code < 256 else 0
    if key == chr(27):
        exit()
    shiftvec = Vec2(0,0)
    if key == 'w':
        shiftvec = Vec2(sin(playerangle.x) * SPEED, cos(playerangle.x) * SPEED)
        playerpos += shiftvec
    elif key == 's':
        shiftvec = Vec2(-sin(playerangle.x) * SPEED, -cos(playerangle.x) * SPEED)
        playerpos += shiftvec
    elif key == 'a':
        playerangle -= Vec2(ROTATION_SPEED, 0)
    elif key == 'd':
        playerangle += Vec2(ROTATION_SPEED, 0)
    elif key == 'r':
        playerangle += Vec2(0, degrees(ROTATION_SPEED))
    elif key == 'f':
        playerangle -= Vec2(0, degrees(ROTATION_SPEED))

    if not world.get_block(playerpos) in (" ", "?", ".", "S", "E"):
        playerpos -= shiftvec

if __name__ == "__main__":
    print("Testing vec2")
    print(f"Vec2(1,1) + 1 = {Vec2(1,1) + 1}")
    print(f"Vec2(1,1) + Vec2(1,2) = {Vec2(1, 1) + Vec2(1,2)}")
    print(f"Vec2(3,1).x = {Vec2(3,1).x}")
    print(f"round(Vec2(1.1,1.6), 2) = {round(Vec2(1.1, 1.6), 2)}")
    print(f"round(Vec2(1.1,1.6)) = {round(Vec2(1.1, 1.6))}")

