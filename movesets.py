
from attacks import Attack, HitBox


class MoveSet1:

    max_vel_x = 12
    gravity = 2
    num_jumps = 2
    jump_vel = 28
    jumpsquat = 4

    class Jab(Attack):
        total_frames = 20

        def init_hitboxes(self):
            return [HitBox(x=50, y=0, r=20, hitstun=10, damage=4)]

    class ForwardSmash(Attack):
        total_frames = 30
        startup_frames = 10

        def init_hitboxes(self):
            return [HitBox(x=70, y=10, r=50, send_angle=20, send_power=20, damage=23)]

    class UpSmash(Attack):
        total_frames = 40

        def init_hitboxes(self):
            hitbox1 = HitBox(x=10, y=70, r=40, damage=20)
            hitbox1.sa_func = lambda t: t * 9
            hitbox1.sp_func = lambda t: 5 + t // 3
            return [hitbox1]

    class DownSmash(Attack):
        total_frames = 30

        def init_hitboxes(self):
            hitbox1 = HitBox(y=-25, r=20, send_angle=190, send_power=12, damage=15)
            hitbox1.x_func = lambda t: -3 * t
            hitbox2 = HitBox(y=-28, r=15, send_angle=350, send_power=11, damage=15)
            hitbox2.x_func = lambda t: 3 * t
            return [hitbox1, hitbox2]

    class ForwardTilt(Attack):
        total_frames = 20

        def init_hitboxes(self):
            return [HitBox(x=40, y=0, r=10, send_angle=10, send_power=8)]

    class UpTilt(Attack):
        total_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(y=50, r=35, send_angle=90, send_power=12)
            hitbox1.x_func = lambda t: 40 - 4 * t
            return [hitbox1]

    class DownTilt(Attack):
        total_frames = 20

        def init_hitboxes(self):
            return [HitBox(x=30, y=-20, r=20, send_angle=40, send_power=8),
                    HitBox(x=60, y=-25, r=15, send_angle=90, send_power=6)]

    class NeutralAir(Attack):
        total_frames = 10

        def init_hitboxes(self):
            return [HitBox(x=30, y=0, r=30, send_angle=30, send_power=8),
                    HitBox(x=-30, y=0, r=25, send_angle=150, send_power=8)]

    class ForwardAir(Attack):
        total_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(r=20, send_angle=90, send_power=4, damage=9)
            hitbox1.x_func = lambda t: 70 - (t - 10) ** 2
            hitbox1.y_func = lambda t: 10 * (t - 10)
            return [hitbox1]

    class BackAir(Attack):
        total_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(r=30, send_angle=150, damage=11)
            hitbox1.x_func = lambda t: -2 * t - 50
            hitbox1.y_func = lambda t: t
            hitbox1.sp_func = lambda t: t // 3 + 4
            return [hitbox1]

    class UpAir(Attack):
        total_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(r=20, send_angle=90, send_power=4, damage=8)
            hitbox1.x_func = lambda t: 10 * (t - 10)
            hitbox1.y_func = lambda t: 70 - (t - 10) ** 2
            return [hitbox1]

    class DownAir(Attack):
        total_frames = 30

        def init_hitboxes(self):
            hitbox1 = HitBox(x=0, y=-30, r=15, send_angle=90, send_power=2, damage=5)
            hitbox2 = HitBox(x=0, y=-60, r=30, send_angle=-90, send_power=4, damage=15)
            hitbox2.ia_func = lambda t: 15 < t < 25
            return [hitbox1, hitbox2]

    class NeutralSpecial(Attack):
        total_frames = 50

        def init_hitboxes(self):
            hitbox1 = HitBox(y=0, r=20, send_angle=60, send_power=4, damage=10)
            hitbox1.x_func = lambda t: 10 * t
            hitbox2 = HitBox(y=0, r=15, send_angle=60, send_power=3, damage=9)
            hitbox2.x_func = lambda t: -10 * t
            return [hitbox1, hitbox2]

    class ForwardSpecial(Attack):
        total_frames = 60

        def init_hitboxes(self):
            hitbox1 = HitBox(x=500, r=20, send_angle=60, damage=5)
            hitbox1.r_func = lambda t: t
            hitbox1.sp_func = lambda t: t // 4 + 2
            return [hitbox1]

    class UpSpecial(Attack):
        total_frames = 30
        vel_x = 2
        vel_y = 14

        def init_hitboxes(self):
            return [HitBox(x=15, y=80, r=70, send_angle=90, send_power=8)]

    class DownSpecial(Attack):
        total_frames = 30
        vel_y = -10

        def init_hitboxes(self):
            return [HitBox(x=30, y=-80, r=40, send_angle=270, send_power=15),
                    HitBox(x=-30, y=-70, r=35, send_angle=320, send_power=20)]
