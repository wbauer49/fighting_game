import math

import movesets
import controllers
import definitions
import rendering


class Player(definitions.Object):
    is_facing_right = True
    is_airborne = True
    is_running = False

    airdodge_frames = 0
    attack_frames = 0
    stun_frames = 0
    jumpsquat_frames = 0
    paused_frames = 0

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

    def get_color(self):
        if self.attack_frames:
            return definitions.Color(30, 30, 1)
        elif self.airdodge_frames:
            return definitions.Color(100, 1, 100)
        elif self.stun_frames:
            return definitions.Color(100, 1, 1)
        elif self.jumpsquat_frames:
            return definitions.Color(1, 50, 50)
        elif self.paused_frames:
            return definitions.Color(100, 100, 100)
        else:
            return definitions.Color(1, 1, 1)

    def calculate_update(self):
        self.prev_ctrl = self.curr_ctrl
        self.curr_ctrl = self.controller.get_ctrl_frame()

        if self.paused_frames > 0:
            self.paused_frames -= 1
            return

        # hit_ground check
        # TODO: move checks like hit_ground, is_airborne, etc. to be assigned in function here
        hit_ground = False
        if self.y < -rendering.HEIGHT // 2 + self.r:
            hit_ground = True
            self.y = -rendering.HEIGHT // 2 + self.r
            self.vel_y = 0
            self.is_airborne = False

        elif self.y > rendering.HEIGHT * 3 // 2:
            self.respawn()
            return

        if self.airdodge_frames > 0:
            self.airdodge_frames -= 1
            self.x += self.vel_x
            self.y += self.vel_y
            if hit_ground:
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
                self.remaining_jumps = self.num_jumps - 1
                self.vel_y = 20
                self.is_airborne = True
            return

        for hitbox in self.sub_objects:
            hitbox.step()

        self.apply_movement()

        if self.stun_frames > 0:
            self.stun_frames -= 1
            return

        if self.attack_frames > 0:
            if hit_ground or self.attack_frames == 1:
                self.sub_objects = []
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

            ):  # TODO: make sure this doesn't immediately double jump
                self.remaining_jumps -= 1
                self.vel_y = 20

            if (
                    (self.curr_ctrl.l >= 80 and self.prev_ctrl.l < 80) or
                    (self.curr_ctrl.r >= 80 and self.prev_ctrl.r < 80)
            ):
                self.airdodge_frames = 14
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
                    self.start_attack(self.moveset.UpAir)
                else:
                    raise Exception("Error in c-stick aerial attack execution.")
                return

            return

        if (
                (self.curr_ctrl.x and not self.prev_ctrl.x) or
                (self.curr_ctrl.y and not self.prev_ctrl.y) or
                (self.curr_ctrl.m_y > 50 and self.curr_ctrl.m_y - self.prev_ctrl.m_y >= 10)
        ):
            self.jumpsquat_frames = 3
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
        self.x += self.vel_x

        if self.x > rendering.WIDTH // 2 - self.r:
            self.vel_x = -abs(self.vel_x)
            self.x = rendering.WIDTH // 2 - self.r
        elif self.x < -(rendering.WIDTH // 2 - self.r):
            self.vel_x = abs(self.vel_x)
            self.x = -(rendering.WIDTH // 2 - self.r)

        if self.stun_frames > 0:
            pass

        elif self.attack_frames > 0 or abs(self.curr_ctrl.m_x) < 20:
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

        self.y += self.vel_y
        if self.is_airborne and self.airdodge_frames == 0:
            self.vel_y -= self.gravity

    def start_attack(self, attack):
        self.curr_attack = attack(self.is_facing_right)
        self.attack_frames = self.curr_attack.num_frames
        self.sub_objects = self.curr_attack.hitboxes

    def apply_hitbox(self, hitbox):
        self.is_airborne = True
        self.stun_frames = round(hitbox.hitstun)
        power = round((50 + self.damage_taken) * hitbox.send_power / 30)
        self.vel_x = round(power * math.cos(math.radians(hitbox.send_angle)))
        self.vel_y = round(power * math.sin(math.radians(hitbox.send_angle)))
        self.damage_taken += hitbox.damage
        hitbox.hit_player = True
        print(self.damage_taken)
