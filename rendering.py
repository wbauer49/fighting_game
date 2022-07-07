import pygame


WIDTH = 1400
HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)


class Renderer:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()

    def render(self, objects):
        self.screen.fill(BACKGROUND_COLOR)
        for obj in objects:
            self.render_object(obj)

    def render_object(self, obj, x_offset=0, y_offset=0):
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_colorkey((0, 0, 0))
        surface.set_alpha(obj.color.a)

        center_x = WIDTH / 2 + obj.get_x() + x_offset
        center_y = HEIGHT / 2 - obj.get_y() - y_offset
        pygame.draw.circle(surface, obj.get_color().as_tuple(), (center_x, center_y), obj.r)
        self.screen.blit(surface, (0, 0))

        for sub_object in obj.sub_objects:
            self.render_object(sub_object, x_offset=(obj.get_x() + x_offset), y_offset=(obj.get_y() + y_offset))
