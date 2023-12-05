
import pygame


class CtrlFrame:
    
    def __init__(self, a=False, b=False, x=False, y=False, z=False, start=False, 
                 m_x=0, m_y=0, c_x=0, c_y=0, l=0, r=0):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.z = z
        self.start = start

        m_x = min(100, max(-100, round(m_x)))
        m_y = min(100, max(-100, round(m_y)))
        m_r = max(1, (m_x ** 2 + m_y ** 2) ** 0.5)
        self.m_x = round(m_x / m_r)
        self.m_y = round(m_y / m_r)

        c_x = min(100, max(-100, round(c_x)))
        c_y = min(100, max(-100, round(c_y)))
        c_r = max(1, (c_x ** 2 + c_y ** 2) ** 0.5)
        self. c_x = round(c_x / c_r)
        self. c_y = round(c_y / c_r)

        self.l = min(100, max(0, round(l)))
        self.r = min(100, max(0, round(r)))


class GameCubeController:

    def __init__(self, player_num=1):
        self.player_num = player_num
        self.joystick = pygame.joystick.Joystick(pygame.joystick.get_count() - player_num)
        self.joystick.init()

    def get_ctrl_frame(self):
        return CtrlFrame(
            a=self.joystick.get_button(1),
            b=self.joystick.get_button(2),
            x=self.joystick.get_button(0),
            y=self.joystick.get_button(3),
            z=self.joystick.get_button(7),
            start=self.joystick.get_button(9),
            m_x=round(140 * self.joystick.get_axis(0)),
            m_y=round(-140 * self.joystick.get_axis(1)),
            c_x=round(140 * self.joystick.get_axis(5)),
            c_y=round(-140 * self.joystick.get_axis(2)),
            l=round(100 * self.joystick.get_axis(3)) + 100,
            r=round(100 * self.joystick.get_axis(4)) + 100,
        )


class CpuController:

    def __init__(self, body):
        self.body = body

    def get_ctrl_frame(self):
        b = False
        x = False
        m_x = 0
        m_y = 0

        if self.body.x < -100:
            m_x = 60
        elif self.body.x > 100:
            m_x = -60

        if self.body.y < -250:
            if self.body.remaining_jumps == 0:
                m_y = 70
                b = True
            else:
                x = True

        return CtrlFrame(b=b, x=x, m_x=m_x, m_y=m_y)
