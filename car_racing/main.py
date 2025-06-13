import pygame
from .constants import (
    GRASS,
    TRACK,
    TRACK_BORDER,
    TRACK_BORDER_MASK,
    FINISH,
    FINISH_MASK,
    FINISH_POSITION,
    WIN,
    FPS,
    PATH,
    MAIN_FONT,
    HEIGHT,
)
from .utils import blit_text_center
from .models.player_car import PlayerCar
from .models.computer_car import ComputerCar
from .models.game_info import GameInfo

pygame.display.set_caption("Racing Game!")


def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(
        f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255)
    )
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255)
    )
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    # WASD controls
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide is not None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide is not None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)


def main():
    run = True
    clock = pygame.time.Clock()
    images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0)),
        (FINISH, FINISH_POSITION),
        (TRACK_BORDER, (0, 0)),
    ]
    player_car = PlayerCar(4, 4)
    computer_car = ComputerCar(2, 4, PATH)
    game_info = GameInfo()

    while run:
        clock.tick(FPS)

        draw(WIN, images, player_car, computer_car, game_info)

        while not game_info.started:
            blit_text_center(
                WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!"
            )
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        move_player(player_car)
        computer_car.move()

        handle_collision(player_car, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.reset()

    pygame.quit()


if __name__ == "__main__":
    main()
