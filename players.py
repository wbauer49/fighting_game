
import math

import controllers
import definitions
import env
import rendering


class Player(definitions.Object):
    is_facing_right = True
    is_airborne = True
    is_running = False

    vel_y = 0
    vel_x = 0
    damage_taken = 0
    remaining_jumps = 0

    airdodge_frames = 0
    attack_frames = 0
    stun_frames = 0
    jumpsquat_frames = 0
    paused_frames = 0

    curr_attack = None
    curr_platform = None

    def __init__(self, player_num, moveset):
        self.player_num = player_num
        self.moveset = moveset

        if player_num == 0:
            self.controller = controllers.CpuController(self)
        else:
            self.controller = controllers.GameCubeController(player_num=player_num)
        self.curr_ctrl = self.controller.get_ctrl_frame()
        self.prev_ctrl = self.controller.get_ctrl_frame()

        self.eye = definitions.Object()
        self.eye.x = 20
        self.eye.y = 10
        self.eye.r = 5
        self.eye.color = definitions.Color(200, 200, 200)

    def respawn(self):
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.is_facing_right = True
        self.is_airborne = True
        self.is_running = False
        self.curr_attack = None
        self.damage_taken = 0
        self.attack_frames = 0
        self.stun_frames = 0
        self.paused_frames = 10
        self.remaining_jumps = self.moveset.num_jumps - 1

    def get_hitboxes(self):
        if self.curr_attack is not None:
            return self.curr_attack.hitboxes
        else:
            return []

    def get_sub_objects(self):
        self.eye.x = 20 if self.is_facing_right else -20
        return self.get_hitboxes() + [self.eye]

    def get_color(self):
        if self.paused_frames:
            return definitions.Color(100, 100, 100)
        elif self.stun_frames:
            return definitions.Color(100, 1, 1)
        elif self.airdodge_frames:
            return definitions.Color(100, 1, 100)
        elif self.attack_frames:
            return definitions.Color(30, 30, 1)
        elif self.jumpsquat_frames:
            return definitions.Color(1, 50, 50)

        else:
            return definitions.Color(1, 1, 1)

    def check_hit_ground(self):
        for platform in env.stage.platforms:
            if platform.x - platform.w // 2 <= self.x <= platform.x + platform.w // 2:
                # if platform.is_solid:
                #     if platform.y - platform.h // 2 <= self.y + self.r <= platform.y + platform.h // 2:
                #         self.vel_y = 0
                #     self.y = platform.y - platform.h // 2 - self.r
                if (
                        self.y - self.r < platform.y + platform.h // 2 and
                        self.y > platform.y - platform.h // 2 and
                        self.y - self.r - self.vel_y >= platform.y + platform.h // 2
                ):
                    self.y = platform.y + platform.h // 2 + self.r
                    self.vel_y = 0
                    self.is_airborne = False
                    self.curr_platform = platform
                    return True
        return False

    def calculate_update(self):
        self.prev_ctrl = self.curr_ctrl
        self.curr_ctrl = self.controller.get_ctrl_frame()

        if self.paused_frames > 0:
            self.paused_frames -= 1
            return

        if (
                self.x > rendering.WIDTH or self.x < -rendering.WIDTH or
                self.y > rendering.HEIGHT or self.y < -rendering.HEIGHT
        ):
            self.respawn()
            return

        if self.airdodge_frames > 0:
            self.airdodge_frames -= 1
            self.x += self.vel_x
            self.y += self.vel_y
            if self.check_hit_ground():
                self.airdodge_frames = min(3, self.airdodge_frames)
                return

            if self.airdodge_frames == 0 and self.is_airborne:
                self.vel_x = 0
                self.vel_y = 0
                self.paused_frames = 6
            return

        if self.jumpsquat_frames > 0:
            self.jumpsquat_frames -= 1

            if self.jumpsquat_frames == 0:
                self.remaining_jumps = self.moveset.num_jumps - 1
                self.vel_y = self.moveset.jump_vel
                self.curr_platform = None
                self.is_airborne = True
            return

        if self.curr_platform and (
                self.x < self.curr_platform.x - self.curr_platform.w // 2 or
                self.x > self.curr_platform.x + self.curr_platform.w // 2
        ):
            self.curr_platform = None
            self.is_airborne = True

        self.apply_movement()
        hit_ground = self.check_hit_ground()

        if self.stun_frames > 0:
            self.stun_frames -= 1
            return

        if self.attack_frames > 0:
            self.curr_attack.step()
            if hit_ground or self.attack_frames == 1:
                self.curr_attack = None
                self.attack_frames = 0
            else:
                self.attack_frames -= 1
            return

        if self.curr_ctrl.b and not self.prev_ctrl.b:
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
            return

        if self.is_airborne:
            if self.remaining_jumps > 0 and (
                    (self.curr_ctrl.x and not self.prev_ctrl.x) or
                    (self.curr_ctrl.y and not self.prev_ctrl.y) or
                    (self.curr_ctrl.m_y > 50 and self.curr_ctrl.m_y - self.prev_ctrl.m_y >= 10)
            ):  # TODO: make sure this doesn't immediately double jump (for 3-jump chars)
                self.remaining_jumps -= 1
                self.vel_y = self.moveset.jump_vel

            if (
                    (self.curr_ctrl.l >= 80 and self.prev_ctrl.l < 80) or
                    (self.curr_ctrl.r >= 80 and self.prev_ctrl.r < 80)
            ):
                self.airdodge_frames = 10
                self.vel_x = self.curr_ctrl.m_x // 5
                self.vel_y = self.curr_ctrl.m_y // 5
                return

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
                return

            if abs(self.curr_ctrl.c_x) > 50 or abs(self.curr_ctrl.c_y) > 50:
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
                    self.start_attack(self.moveset.DownAir)
                else:
                    raise Exception("Error in c-stick aerial attack execution.")
                return

            return

        if (
                (self.curr_ctrl.x and not self.prev_ctrl.x) or
                (self.curr_ctrl.y and not self.prev_ctrl.y) or
                (self.curr_ctrl.m_y > 50 and self.curr_ctrl.m_y - self.prev_ctrl.m_y >= 10)
        ):
            self.jumpsquat_frames = self.moveset.jumpsquat
            self.vel_y = 0

        if self.curr_ctrl.a and not self.prev_ctrl.a:
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
            return

        if abs(self.curr_ctrl.c_x) > 50 or abs(self.curr_ctrl.c_y) > 50:
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
            return

    def apply_movement(self):

        if self.curr_attack:
            if self.curr_attack.vel_x is not None:
                self.vel_x = self.curr_attack.vel_x
            if self.curr_attack.vel_y is not None:
                self.vel_y = self.curr_attack.vel_y

        self.x += self.vel_x

        if self.x > rendering.WIDTH // 2 - self.r:
            self.vel_x = 0
            self.x = rendering.WIDTH // 2 - self.r
        elif self.x < -(rendering.WIDTH // 2 - self.r):
            self.vel_x = 0
            self.x = -(rendering.WIDTH // 2 - self.r)

        elif not self.is_airborne and (self.attack_frames > 0 or abs(self.curr_ctrl.m_x) < 20):
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

            self.vel_x = min(self.moveset.max_vel_x, max(-self.moveset.max_vel_x, self.vel_x + accel_dir * accel))
            if not self.is_airborne:
                if self.vel_x < 0:
                    self.is_facing_right = False
                elif self.vel_x > 0:
                    self.is_facing_right = True

                if self.vel_x == self.moveset.max_vel_x or self.vel_x == -self.moveset.max_vel_x:
                    self.is_running = True

        self.y += self.vel_y
        if self.is_airborne and self.airdodge_frames == 0:
            if self.stun_frames > 0:
                self.vel_y -= self.moveset.gravity // 2
            else:
                self.vel_y -= self.moveset.gravity

    def start_attack(self, attack):
        self.curr_attack = attack(self.is_facing_right)
        self.attack_frames = self.curr_attack.total_frames

    def apply_hitbox(self, hitbox):
        self.is_airborne = True
        self.stun_frames = round(hitbox.hitstun * (self.damage_taken / 50 + 1) * (hitbox.damage / 10))
        power = 1 + self.damage_taken * hitbox.send_power // 40
        self.vel_x = round(power * math.cos(math.radians(hitbox.send_angle)))
        self.vel_y = round(power * math.sin(math.radians(hitbox.send_angle))) + self.moveset.gravity * 2
        self.damage_taken += hitbox.damage
        hitbox.hit_player = True
