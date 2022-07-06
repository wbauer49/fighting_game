
import definitions


def apply_hitboxes(attacker, receiver):
    for hitbox in attacker.sub_objects:
        if hitbox.hit_player or not hitbox.is_active:
            continue

        distance = round(((attacker.x + hitbox.get_x() - receiver.x) ** 2 + (attacker.y + hitbox.get_y() - receiver.y) ** 2) ** 0.5)
        if attacker.r + receiver.r > distance:
            receiver.apply_hitbox(hitbox)
            break


class HitBox(definitions.Object):
    frame = 0
    c = definitions.Color(150, 150, 150)
    damage = 10
    is_facing_right = True

    send_angle = 0
    send_power = 1
    hitstun = 10

    x = 0
    y = 0
    r = 10
    is_active = True
    hit_player = False

    x_func = None
    y_func = None
    r_func = None
    is_active_func = None

    def __init__(self, x=0, y=0, r=10, send_angle=0, send_power=1):
        self.x = x
        self.y = y
        self.r = r
        self.send_angle = send_angle
        self.send_power = send_power

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
        if self.is_active_func:
            self.is_active = self.is_active_func(t)

    def get_x(self):
        return self.x if self.is_facing_right else -self.x


class Attack:
    num_frames = None

    def __init__(self, is_facing_right):
        self.is_facing_right = is_facing_right

        self.hitboxes = self.init_hitboxes()
        if not self.is_facing_right:
            for hitbox in self.hitboxes:
                hitbox.is_facing_right = self.is_facing_right
                hitbox.send_angle = (180 - hitbox.send_angle) % 360

    def init_hitboxes(self):
        return []


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

    class UpTilt(Attack):
        num_frames = 20

        def init_hitboxes(self):
            hitbox1 = HitBox(y=50, r=35, send_angle=90, send_power=10)
            hitbox1.x_func = lambda t: 40 - 4 * t
            return [hitbox1]

    class DownTilt(Attack):
        num_frames = 20

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

    class ForwardSpecial(Attack):
        num_frames = 20

    class UpSpecial(Attack):
        num_frames = 20

    class DownSpecial(Attack):
        num_frames = 20
