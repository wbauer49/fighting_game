
import pygame

import definitions
import rendering

renderer = rendering.Renderer()
obj = definitions.Object()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

    update = obj.calculate_update()
    obj.apply_update(update)
    renderer.render(obj)
    pygame.display.flip()

pygame.quit()
