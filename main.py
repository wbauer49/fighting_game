
import pygame
import time

import attacks
import player
import rendering


try:
    renderer = rendering.Renderer()
    player1 = player.Player(player_num=1)
    player2 = player.Player(player_num=2)
    objects = [player2, player1]

    pygame.init()
    running = True
    while running:
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        for obj in objects:
            obj.calculate_update()
            obj.update_sub_objects()
        renderer.render(objects)

        pygame.display.flip()

        attacks.apply_hitboxes(player1, player2)
        attacks.apply_hitboxes(player2, player1)

        sleep_time = (1 / 60) - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("frame lag")

except KeyboardInterrupt:
    print("exited")
finally:
    pygame.quit()
