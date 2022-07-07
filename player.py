import math

import movesets
import controllers
import definitions
import rendering


class Player(definitions.Object):

    is_facing_right = True
    is_airborne = True
    is_running = False

    attack_frames = 0
    stun_frames = 5
    curr_attack = None
    damage_taken = 0

    vel_y = 0
    vel_x = 0
    max_vel_x = 12
    gravity = 2

    moveset = movesets.MoveSet()
    num_jumps = 2
    remaining_jumps = 2

    def __init__(self, player_num):
        self.player_num = player_num
        self.controller = controllers.GameCubeController(player_num=player_num)
        self.curr_ctrl = self.controller.get_ctrl_frame()
        self.prev_ctrl = self.controller.get_ctrl_frame()

    def get_color(self):
        if self.stun_frames > 0:
            return definitions.Color(100, 1, 1)
        else:
            return definitions.Color(1, 1, 1)

    def calculate_update(self):
        self.prev_ctrl = self.curr_ctrl
        self.curr_ctrl = self.controller.get_ctrl_frame()

        for hitbox in self.sub_objects:
            hitbox.step()

        self.horizontal_movement()
        hit_ground = self.apply_gravity()

        if self.stun_frames > 0:
            self.stun_frames -= 1

        elif self.attack_frames > 0:
            if hit_ground or self.attack_frames == 1:
                self.sub_objects = []
                self.curr_attack = None
                self.attack_frames = 0
            else:
                self.attack_frames -= 1

        elif self.is_airborne:
            if self.remaining_jumps > 0 and (
                    (self.curr_ctrl.x and not self.prev_ctrl.x) or
                    (self.curr_ctrl.y and not self.prev_ctrl.y) or
                    (self.curr_ctrl.m_y > 50 and self.curr_ctrl.m_y - self.prev_ctrl.m_y >= 10)
            ):
                self.remaining_jumps -= 1
                self.vel_y = 20

            if self.curr_ctrl.a and not self.prev_ctrl.a:
                if abs(self.curr_ctrl.m_x) < 20 and abs(self.curr_ctrl.m_y) < 20:
                    self.start_attack(self.moveset.NeutralAir)
                elif self.curr_ctrl.m_x > abs(self.curr_ctrl.m_y):
                    if self.is_facing_right:
                        self.start_attack(self.moveset.ForwardAir)
                    else:
                        self.start_attack(self.moveset.BackAir)
                elif self.curr_ctrl.m_x < -abs(self.curr_ctrl.m_y):
                    if self.is_facing_right:
                        self.start_attack(self.moveset.BackAir)
                    else:
                        self.start_attack(self.moveset.ForwardAir)
                elif self.curr_ctrl.m_y >= abs(self.curr_ctrl.m_x):
                    self.start_attack(self.moveset.UpAir)
                elif self.curr_ctrl.m_y <= -abs(self.curr_ctrl.m_x):
                    self.start_attack(self.moveset.DownAir)
                else:
                    raise Exception("Error in a-button aerial attack execution.")

            elif abs(self.curr_ctrl.c_x) > 50 or abs(self.curr_ctrl.c_y) > 50:
                if self.curr_ctrl.c_x > abs(self.curr_ctrl.c_y):
                    if self.is_facing_right:
                        self.start_attack(self.moveset.ForwardAir)
                    else:
                        self.start_attack(self.moveset.BackAir)
                elif self.curr_ctrl.c_x < -abs(self.curr_ctrl.c_y):
                    if self.is_facing_right:
                        self.start_attack(self.moveset.BackAir)
                    else:
                        self.start_attack(self.moveset.ForwardAir)
                elif self.curr_ctrl.c_y >= abs(self.curr_ctrl.c_x):
                    self.start_attack(self.moveset.UpAir)
                elif self.curr_ctrl.c_y <= -abs(self.curr_ctrl.c_x):
                    self.start_attack(self.moveset.UpAir)
                else:
                    raise Exception("Error in c-stick aerial attack execution.")

        elif (
                (self.curr_ctrl.x and not self.prev_ctrl.x) or
                (self.curr_ctrl.y and not self.prev_ctrl.y) or
                (self.curr_ctrl.m_y > 50 and self.curr_ctrl.m_y - self.prev_ctrl.m_y >= 10)
        ):
            self.is_airborne = True
            self.remaining_jumps = self.num_jumps - 1
            self.vel_y = 20

        elif self.curr_ctrl.a and not self.prev_ctrl.a:
            if abs(self.curr_ctrl.m_x) < 20 and abs(self.curr_ctrl.m_y) < 20:
                self.start_attack(self.moveset.Jab)
            elif self.curr_ctrl.m_x > abs(self.curr_ctrl.m_y):
                self.is_facing_right = True
                self.start_attack(self.moveset.ForwardTilt)
            elif self.curr_ctrl.m_x < -abs(self.curr_ctrl.m_y):
                self.is_facing_right = False
                self.start_attack(self.moveset.ForwardTilt)
            elif self.curr_ctrl.m_y >= abs(self.curr_ctrl.m_x):
                self.start_attack(self.moveset.UpTilt)
            elif self.curr_ctrl.m_y <= -abs(self.curr_ctrl.m_x):
                self.start_attack(self.moveset.DownTilt)
            else:
                raise Exception("Error in tilt attack execution.")

        elif self.curr_ctrl.b and not self.prev_ctrl.b:
            if abs(self.curr_ctrl.m_x) < 20 and abs(self.curr_ctrl.m_y) < 20:
                self.start_attack(self.moveset.NeutralSpecial)
            elif self.curr_ctrl.m_x > abs(self.curr_ctrl.m_y):
                self.is_facing_right = True
                self.start_attack(self.moveset.ForwardSpecial)
            elif self.curr_ctrl.m_x < -abs(self.curr_ctrl.m_y):
                self.is_facing_right = False
                self.start_attack(self.moveset.ForwardSpecial)
            elif self.curr_ctrl.m_y >= abs(self.curr_ctrl.m_x):
                self.start_attack(self.moveset.UpSpecial)
            elif self.curr_ctrl.m_y <= -abs(self.curr_ctrl.m_x):
                self.start_attack(self.moveset.DownSpecial)
            else:
                raise Exception("Error in special attack execution.")

        elif abs(self.curr_ctrl.c_x) > 50 or abs(self.curr_ctrl.c_x) > 50:
            if self.curr_ctrl.c_x > abs(self.curr_ctrl.c_y):
                self.is_facing_right = True
                self.start_attack(self.moveset.ForwardSmash)
            elif self.curr_ctrl.c_x < -abs(self.curr_ctrl.c_y):
                self.is_facing_right = False
                self.start_attack(self.moveset.ForwardSmash)
            elif self.curr_ctrl.c_y >= abs(self.curr_ctrl.c_x):
                self.start_attack(self.moveset.UpSmash)
            elif self.curr_ctrl.c_y <= -abs(self.curr_ctrl.c_x):
                self.start_attack(self.moveset.DownSmash)
            else:
                raise Exception("Error in smash attack execution.")

    def horizontal_movement(self):
        self.x += self.vel_x

        if self.x > rendering.WIDTH // 2 - self.r:
            self.vel_x = -abs(self.vel_x)
            self.x = rendering.WIDTH // 2 - self.r
        elif self.x < -(rendering.WIDTH // 2 - self.r):
            self.vel_x = abs(self.vel_x)
            self.x = -(rendering.WIDTH // 2 - self.r)

        if self.stun_frames > 0:
            pass

        elif self.attack_frames > 0 or abs(self.curr_ctrl.m_x) < 10:
            if self.vel_x > 0:
                self.vel_x -= 1
            elif self.vel_x < 0:
                self.vel_x += 1

        else:
            if abs(self.curr_ctrl.m_x) < 10:
                accel_dir = 0
                accel = 0
            else:
                accel_dir = 1 if self.curr_ctrl.m_x > 0 else -1
                accel = (abs(self.curr_ctrl.m_x) - 10) // 30

            self.vel_x = min(self.max_vel_x, max(-self.max_vel_x, self.vel_x + accel_dir * accel))
            if not self.is_airborne:
                if self.vel_x < 0:
                    self.is_facing_right = False
                elif self.vel_x > 0:
                    self.is_facing_right = True

                if self.vel_x == self.max_vel_x or self.vel_x == -self.max_vel_x:
                    self.is_running = True

    def apply_gravity(self):
        self.y += self.vel_y

        if self.is_airborne:
            self.vel_y -= self.gravity

            if self.y <= -rendering.HEIGHT // 2 + self.r:
                self.is_airborne = False
                self.y = -rendering.HEIGHT // 2 + self.r
                self.vel_y = 0
                return True

        return False

    def start_attack(self, attack):
        self.curr_attack = attack(self.is_facing_right)
        self.attack_frames = self.curr_attack.num_frames
        self.sub_objects = self.curr_attack.hitboxes

    def apply_hitbox(self, hitbox):
        self.is_airborne = True
        self.stun_frames = round(hitbox.hitstun)
        power = round((50 + self.damage_taken) * hitbox.send_power / 30)
        self.vel_x = power * math.cos(math.radians(hitbox.send_angle))
        self.vel_y = power * math.sin(math.radians(hitbox.send_angle))
        self.damage_taken += hitbox.damage
        hitbox.hit_player = True
        print(self.damage_taken)
