
import attacks
import controllers
import definitions


class Player(definitions.Object):

    is_facing_right = True
    is_airborne = False
    is_running = False
    attack_frames = 0
    stun_frames = 5
    curr_attack = None
    vel_y = 0
    gravity = 5
    moveset = attacks.MoveSet()
    num_jumps = 2
    remaining_jumps = 2

    def __init__(self, player_num):
        self.player_num = player_num
        self.controller = controllers.GameCubeController(player_num=player_num)
        self.curr_ctrl = self.controller.get_ctrl_frame()
        self.prev_ctrl = self.controller.get_ctrl_frame()

    def apply_gravity(self):
        self.y += self.vel_y

        if self.is_airborne:
            self.vel_y -= self.gravity

            if self.y <= 100:
                self.is_airborne = False
                self.y = 100
                self.vel_y = 0
                return True

        return False

    def update_attack(self, attack_frame):
        self.attack_frames.get_attack_frame(attack_frame)

    def start_attack(self, attack):
        self.curr_attack = attack
        self.attack_frames = attack.num_frames

    def calculate_update(self):
        self.prev_ctrl = self.curr_ctrl
        self.curr_ctrl = self.controller.get_ctrl_frame()

        hit_ground = self.apply_gravity()

        if self.stun_frames > 0:
            self.stun_frames -= 1
            return

        if self.attack_frames > 0:
            if hit_ground:
                self.curr_attack = None
                self.attack_frames = 0
            else:
                self.attack_frames -= 1
                self.update_attack(self.attack_frames)
                return

        if self.is_airborne:
            if self.remaining_jumps > 0 and (
                    (self.curr_ctrl.x and not self.prev_ctrl.x) or
                    (self.curr_ctrl.y and not self.prev_ctrl.y) or
                    (self.curr_ctrl.m_y > 50 and self.curr_ctrl.m_y - self.prev_ctrl.m_y >= 10)
            ):
                self.is_airborne = True
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
