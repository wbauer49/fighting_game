
import definitions


class Hitmarker(definitions.Object):

    finished = False

    def __init__(self, attacker, hitbox):
        self.x = attacker.x + hitbox.get_x()
        self.y = attacker.y + hitbox.get_y()
        self.r = hitbox.r
        self.color = hitbox.get_color()
        self.color.a //= 3

        self.expand_r = self.r // 3

    def step(self):
        self.r += self.expand_r
        self.color.a -= 2
        if self.color.a <= 0:
            self.finished = True
