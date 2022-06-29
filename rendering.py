import pygame


WIDTH = 1000
HEIGHT = 800


class Renderer:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((255, 255, 255))
        pygame.display.flip()

    def render(self, objects):
        self.screen.fill((255, 255, 255))
        for obj in objects:
            self.render_object(obj)

    def render_object(self, obj):
        pygame.draw.circle(self.screen, obj.c.as_tuple(), (WIDTH / 2 + obj.x, HEIGHT / 2 - obj.y), obj.r)
        for sub_object in obj.sub_objects:
            self.render_object(sub_object)
