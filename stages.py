
import definitions


class Platform:

    color = definitions.Color(20, 20, 20)

    def __init__(self, x, y, w, h, is_solid=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_solid = is_solid


class Stage(definitions.Object):

    platforms = []


class Battlefield(Stage):

    platforms = [
        Platform(0, -200, 1000, 40, is_solid=True),
        Platform(300, 0, 250, 20),
        Platform(-300, 0, 250, 20),
        Platform(0, 200, 250, 20),
    ]
