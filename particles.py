
import definitions


class Hitmarker(definitions.Object):

    finished = False

    def __init__(self, hitbox):
        self.x = hitbox.x
        self.y = hitbox.y
        self.r = hitbox.r
        self.color = hitbox.get_color()
        self.color.a = 50

    def step(self):
        self.r += 5
        self.color.a -= 2
        if self.color.a <= 0:
            self.finished = True
