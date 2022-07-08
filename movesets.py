
from attacks import Attack, HitBox


class MoveSet:

    class Jab(Attack):
        num_frames = 20

        def init_hitboxes(self):
            return [HitBox(x=50, y=0, r=20)]

    class ForwardSmash(Attack):
        num_frames = 20

    class UpSmash(Attack):
        num_frames = 20

    class DownSmash(Attack):
        num_frames = 20

    class ForwardTilt(Attack):
        num_frames = 20

        def init_hitboxes(self):
            return [HitBox(x=40, y=0, r=10, send_angle=10, send_power=8)]

    class UpTilt(Attack):
        num_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(y=50, r=35, send_angle=90, send_power=10)
            hitbox1.x_func = lambda t: 40 - 4 * t
            return [hitbox1]

    class DownTilt(Attack):
        num_frames = 20

        def init_hitboxes(self):
            return [HitBox(x=30, y=-20, r=20, send_angle=40, send_power=8),
                    HitBox(x=60, y=-25, r=15, send_angle=90, send_power=6)]

    class NeutralAir(Attack):
        num_frames = 10

        def init_hitboxes(self):
            return [HitBox(x=30, y=0, r=30, send_angle=30, send_power=8),
                    HitBox(x=-30, y=0, r=30, send_angle=150, send_power=8)]

    class ForwardAir(Attack):
        num_frames = 20

    class BackAir(Attack):
        num_frames = 20

    class UpAir(Attack):
        num_frames = 20

    class DownAir(Attack):
        num_frames = 20

    class NeutralSpecial(Attack):
        num_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(y=0, r=30, send_angle=60, send_power=4)
            hitbox1.x_func = lambda t: t
            hitbox2 = HitBox(y=0, r=30, send_angle=60, send_power=4)
            hitbox2.x_func = lambda t: -t
            return [hitbox1, hitbox2]

    class ForwardSpecial(Attack):
        num_frames = 20

    class UpSpecial(Attack):
        num_frames = 20

    class DownSpecial(Attack):
        num_frames = 20
