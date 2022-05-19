import pygame


class Color:
    def __init__(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def as_tuple(self):
        return self.r, self.g, self.b


class ObjectUpdate:
    dx = 0
    dy = 0


class Object:
    x = 0
    y = 0
    r = 100
    c = Color(0, 0, 0)

    sub_objects = []

    def calculate_update(self):
        return ObjectUpdate()

    def apply_update(self, update):
        self.x += update.dx
        self.y += update.dy


class Player(Object):

    def calculate_update(self):
        r = 10
        c = Color(0, 0, 0)
