import definitions


class HitBox(definitions.Object):
    num_frames = 10
    frame = 0

    x = 0
    y = 0
    r = 10
    active = True

    x_func = None
    y_func = None
    r_func = None
    active_func = None

    @classmethod
    def basic_hitbox(cls, x=0, y=0, r=10, num_frames=10):
        cls.x = x
        cls.y = y
        cls.r = r
        cls.num_frames = num_frames

    def step(self):
        self.frame += 1
        self.calculate_hitbox(self.frame)

    def calculate_hitbox(self, t):
        if self.x_func:
            self.x = self.x_func(t)
        if self.y_func:
            self.y = self.y_func(t)
        if self.r_func:
            self.r = self.r_func(t)
        if self.active_func:
            self.active = self.active_func(t)


class Attack:
    num_frames = None

    def __init__(self):
        self.hitboxes = self.get_hitboxes()
        if self.num_frames is None:
            self.num_frames = max(hitbox.num_frames for hitbox in self.hitboxes)

    def get_hitboxes(self):
        return ()


class MoveSet:
    class Jab(Attack):
        num_frames = 20

        def get_hitboxes(self):
            return HitBox.basic_hitbox(x=100, y=0, r=10, num_frames=10),

    class ForwardSmash(Attack):
        num_frames = 20

    class UpSmash(Attack):
        num_frames = 20

    class DownSmash(Attack):
        num_frames = 20

    class ForwardTilt(Attack):
        num_frames = 20

    class UpTilt(Attack):
        num_frames = 20

    class DownTilt(Attack):
        num_frames = 20

    class NeutralAir(Attack):
        num_frames = 20

    class ForwardAir(Attack):
        num_frames = 20

    class BackAir(Attack):
        num_frames = 20

    class UpAir(Attack):
        num_frames = 20

    class DownAir(Attack):
        num_frames = 20
