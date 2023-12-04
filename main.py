
import pygame
import time

import attacks
import definitions
import env
import movesets
import players
import rendering
import stages


def run_match():

    pygame.init()
    running = True
    while running:
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        for player in env.players:
            player.calculate_update()
            player.update_sub_objects()

        for platform in env.stage.platforms:
            if platform == player1.curr_platform:
                platform.color = definitions.Color(200, 20, 20)
            else:
                platform.color = definitions.Color(20, 20, 20)
        env.renderer.render()

        pygame.display.flip()

        for attacker in env.players:
            for receiver in env.players:
                if receiver != attacker:
                    attacks.apply_hitboxes(attacker, receiver)

        sleep_time = (1 / 60) - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("frame lag")


try:
    env.renderer = rendering.Renderer()
    env.stage = stages.Battlefield

    player1 = players.Player(player_num=1, moveset=movesets.MoveSet1)
    player2 = players.Player(player_num=0, moveset=movesets.MoveSet1)
    env.players = [player1, player2]

    run_match()

except KeyboardInterrupt:
    print("exited")
finally:
    pygame.quit()
