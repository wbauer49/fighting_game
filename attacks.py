
import math

import definitions


def apply_hitboxes(attacker, receiver):

    if attacker.curr_attack is None or attacker.curr_attack.hit_player:
        return

    for hitbox in attacker.get_hitboxes():
        if not hitbox.is_active:
            continue

        distance = round(((attacker.x + hitbox.get_x() - receiver.x) ** 2 +
                          (attacker.y + hitbox.get_y() - receiver.y) ** 2) ** 0.5)
        if hitbox.r + receiver.r > distance:
            receiver.apply_hitbox(hitbox)
            attacker.curr_attack.hit_player = True
            attacker.paused_frames = 3
            receiver.paused_frames = 5
            break


class HitBox(definitions.Object):
    frame = 0
    is_active = True
    is_facing_right = True

    x_func = None
    y_func = None
    r_func = None
    sa_func = None
    sp_func = None
    ia_func = None

    def __init__(self, x=0, y=0, r=10, send_angle=0, send_power=5, damage=10, hitstun=20):
        self.x = x
        self.y = y
        self.r = r
        self.send_angle = send_angle
        self.send_power = send_power
        self.damage = damage
        self.hitstun = hitstun

    def step(self):
        self.frame += 1
        self.calculate_hitbox(self.frame)

    def get_color(self):
        if not self.is_active:
            return definitions.Color(0, 0, 0, a=0)

        alpha = min(255, 70 + 6 * self.send_power)
        angle = math.radians(self.send_angle)
        r = round(120 + 120 * -math.cos(angle))
        g = round(120 + 120 * (math.cos(angle) / 2 + math.sin(angle) * math.sqrt(3) / 2))
        b = round(120 + 120 * (math.cos(angle) / 2 - math.sin(angle) * math.sqrt(3) / 2))

        return definitions.Color(r, g, b, a=alpha)

    def calculate_hitbox(self, t):
        if self.x_func:
            self.x = self.x_func(t)
        if self.y_func:
            self.y = self.y_func(t)
        if self.r_func:
            self.r = self.r_func(t)

        if self.sa_func is not None:
            self.send_angle = self.sa_func(t) if self.is_facing_right else -self.sa_func(t)
        if self.sp_func is not None:
            self.send_power = self.sp_func(t)
        if self.ia_func:
            self.is_active = self.ia_func(t)

    def get_x(self):
        return self.x if self.is_facing_right else -self.x


class Attack:
    total_frames = 20
    startup_frames = 0
    vel_x = None
    vel_y = None
    vx_func = None
    vy_func = None

    frame = 0
    hitboxes = []
    hit_player = False

    def __init__(self, is_facing_right):
        self.is_facing_right = is_facing_right
        if self.vel_x is not None and not self.is_facing_right:
            self.vel_x *= -1

    def init_hitboxes(self):
        return []

    def spawn_hitboxes(self):
        self.hitboxes = self.init_hitboxes()
        for hitbox in self.hitboxes:
            hitbox.calculate_hitbox(0)
            if not self.is_facing_right:
                hitbox.is_facing_right = False
                hitbox.send_angle = (180 - hitbox.send_angle) % 360

    def step(self):
        for hitbox in self.hitboxes:
            hitbox.step()
        if self.frame == self.startup_frames:
            self.spawn_hitboxes()

        self.frame += 1
        self.calculate_attack(self.frame)

    def calculate_attack(self, t):
        if self.vx_func:
            self.vel_x = self.vx_func(t)
        if self.vy_func:
            self.vel_y = self.vy_func(t)
