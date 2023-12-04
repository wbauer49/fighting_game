
import pygame

import env


WIDTH = 1600
HEIGHT = 900
BACKGROUND_COLOR = (255, 255, 255)


class Renderer:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()

        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)

    def render(self):
        self.render_stage()
        self.render_damages()
        for player in env.players:
            self.render_object(player)

    def render_stage(self):
        self.screen.fill(BACKGROUND_COLOR)
        for platform in env.stage.platforms:
            surface = pygame.Surface((platform.w, platform.h))
            surface.fill(platform.color.as_tuple())
            x = WIDTH // 2 + platform.x - platform.w // 2
            y = HEIGHT // 2 - (platform.y + platform.h // 2)
            self.screen.blit(surface, (x, y))

    def render_damages(self):
        for num, player in enumerate(env.players):
            text_surface = self.font.render(str(player.damage_taken), False, (0, 0, 0))
            x_pos = WIDTH * (num + 1) // (len(env.players) + 1) - 20
            self.screen.blit(text_surface, (x_pos, HEIGHT - 100))

    def render_object(self, obj, x_offset=0, y_offset=0):
        if obj.get_color().a == 0:
            return

        surface = pygame.Surface((2 * obj.r, 2 * obj.r))
        surface.set_colorkey((0, 0, 0))
        surface.set_alpha(obj.get_color().a)

        center_x = WIDTH // 2 + obj.get_x() + x_offset
        center_y = HEIGHT // 2 - (obj.get_y() + y_offset)
        pygame.draw.circle(surface, obj.get_color().as_tuple(), (obj.r, obj.r), obj.r)
        self.screen.blit(surface, (center_x - obj.r, center_y - obj.r))

        for sub_object in obj.get_sub_objects():
            self.render_object(sub_object, x_offset=(obj.get_x() + x_offset), y_offset=(obj.get_y() + y_offset))
