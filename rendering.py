import pygame


WIDTH = 1600
HEIGHT = 900
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
        surface = pygame.Surface((2 * obj.r, 2 * obj.r))
        surface.set_colorkey((0, 0, 0))
        surface.set_alpha(obj.get_color().a)

        center_x = WIDTH / 2 + obj.get_x() + x_offset
        center_y = HEIGHT / 2 - obj.get_y() - y_offset
        pygame.draw.circle(surface, obj.get_color().as_tuple(), (obj.r, obj.r), obj.r)
        self.screen.blit(surface, (center_x - obj.r, center_y - obj.r))

        for sub_object in obj.sub_objects:
            self.render_object(sub_object, x_offset=(obj.get_x() + x_offset), y_offset=(obj.get_y() + y_offset))
