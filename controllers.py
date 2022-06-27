
import pygame


class GameCubeController:

    def __init__(self, player_num=1):
        self.player_num = player_num
        self.joystick = pygame.joystick.Joystick(player_num - 1)
        self.joystick.init()

    def get_ctrl_frame(self):
        return CtrlFrame(self.joystick)


class CtrlFrame:

    def __init__(self, joystick):
        self.a = joystick.get_button(1)
        self.b = joystick.get_button(2)
        self.x = joystick.get_button(0)
        self.y = joystick.get_button(3)
        self.z = joystick.get_button(7)
        self.start = joystick.get_button(9)
        self.m_x = round(100 * joystick.get_axis(0))
        self.m_y = round(100 * joystick.get_axis(1))
        self.c_x = round(100 * joystick.get_axis(2))
        self.c_y = round(100 * joystick.get_axis(3))
        self.l = round(100 * joystick.get_axis(4))
        self.r = round(100 * joystick.get_axis(5))
