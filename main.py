
import pygame
import time

import attacks
import definitions
import movesets
import player
import rendering
import stages


def run_match(stage):
    renderer = rendering.Renderer()
    player1 = player.Player(player_num=1, moveset=movesets.MoveSet1, stage=stage)
    player2 = player.Player(player_num=2, moveset=movesets.MoveSet1, stage=stage)
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

        for platform in stage.platforms:
            if platform == player1.curr_platform:
                platform.color = definitions.Color(200, 20, 20)
            else:
                platform.color = definitions.Color(20, 20, 20)
        renderer.render(stage, objects)

        pygame.display.flip()

        attacks.apply_hitboxes(player1, player2)
        attacks.apply_hitboxes(player2, player1)

        sleep_time = (1 / 60) - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("frame lag")


try:
    run_match(stages.Battlefield)
except KeyboardInterrupt:
    print("exited")
finally:
    pygame.quit()
