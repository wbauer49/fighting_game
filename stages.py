import definitions


class Platform:

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
        Platform(0, -250, 900, 40, is_solid=True),
        Platform(300, -50, 200, 20),
        Platform(-300, -50, 200, 20),
        Platform(0, 150, 200, 20),
    ]