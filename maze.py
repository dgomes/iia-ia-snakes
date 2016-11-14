import copy

class Maze:
    def __init__(self, o, p, f):
        self.obstacles = copy.deepcopy(o)
        self.playerpos = copy.deepcopy(p)
        self.foodpos = copy.deepcopy(f)
    def toDict(self):
        return {'obstacles': self.obstacles, 'playerpos': self.playerpos, 'foodpos': self.foodpos}

