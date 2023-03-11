import random

import pygame
import sys

pygame.init()
TILE_LENGTH = 30
NOX_TILES = 25
NOY_TILES = 21
WIDTH = NOX_TILES * TILE_LENGTH
HEIGHT = (NOY_TILES+1.5) * TILE_LENGTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake")
font = pygame.font.Font('freesansbold.ttf', 36)

clock = pygame.time.Clock()


class Board:
    def __init__(self):
        for y in range(NOY_TILES):
            for x in range(NOX_TILES):
                color = "#aaaaaa"
                if (NOY_TILES*y+x) % 2 == 1:
                    color = "#a0a0a0"
                if (x, y) in snake:
                    color = "#3333ff"
                if (x, y) == snake[0]:
                    color = "#0000aa"
                if (x, y) == apple:
                    color = "#ff3333"
                pygame.draw.rect(playZone, color, pygame.Rect(x*TILE_LENGTH, y*TILE_LENGTH, TILE_LENGTH, TILE_LENGTH))
                # Frame(playZone, width=TILE_LENGTH, height=TILE_LENGTH, bg=color).grid(row=y, column=x)

    def update(self):
        self.__init__()


def snake_update(direction):
    global snake_direction
    if direction == "left" and snake_direction not in ["left", "right", "right_x"]:
        snake_direction = "left"
    if direction == "right" and snake_direction not in ["left", "right"]:
        snake_direction = "right"
    if direction == "up" and snake_direction not in ["up", "down"]:
        snake_direction = "up"
    if direction == "down" and snake_direction not in ["up", "down"]:
        snake_direction = "down"


def game_update():
    global snake_length, high_score, snake_alive, apple
    if snake_alive:
        if snake_direction in ["left", "right", "up", "down"]:
            for i in range(len(snake) - 1, 0, -1):
                snake[i] = snake[i - 1]
        if snake_direction == "left":
            snake[0] = (snake[0][0] - 1, snake[0][1])
        if snake_direction == "right":
            snake[0] = (snake[0][0] + 1, snake[0][1])
        if snake_direction == "up":
            snake[0] = (snake[0][0], snake[0][1] - 1)
        if snake_direction == "down":
            snake[0] = (snake[0][0], snake[0][1] + 1)

        if snake[0] == apple:
            snake_length += 1
            if snake_length > high_score:
                high_score = snake_length
            choices = [(x, y) for x in range(NOX_TILES) for y in range(NOY_TILES)]
            for i in snake:
                choices.remove(i)
            apple = random.choice(choices)
            snake.append((69, 69))

        if snake[0] in snake[1:] or not(0 <= snake[0][0] <= NOX_TILES-1) or not(0 <= snake[0][1] <= NOY_TILES-1):
            snake_alive = False

        board.update()
    else:
        screen.blit(restartScreen, rsRect)
        restartScreen.fill("#efefef")
        restartScreen.blit(pygame.image.load("restart.png"), (10, 10))


infoZone = pygame.Surface((WIDTH, TILE_LENGTH*1.5))

playZone = pygame.Surface((WIDTH, HEIGHT-TILE_LENGTH))

restartScreen = pygame.Surface((150, 150))
rsRect = restartScreen.get_rect()
rsRect.center = (WIDTH//2, (HEIGHT-1.5*TILE_LENGTH)//2)


def reset():
    global snake_length, high_score, snake_direction, snake_alive, snake, apple, board
    snake_length = 0
    snake_direction = "right_x"
    snake_alive = True
    snake = [(4 - i, NOY_TILES // 2) for i in range(4)]

    apple = (NOX_TILES - 4, NOY_TILES // 2)

    board = Board()


snake_length = 0

high_score = 0

snake_direction = "right_x"
snake_alive = True
snake = [(4-i, NOY_TILES//2) for i in range(4)]

apple = (NOX_TILES-4, NOY_TILES//2)

board = Board()


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_update("up")
                if event.key == pygame.K_DOWN:
                    snake_update("down")
                if event.key == pygame.K_LEFT:
                    snake_update("left")
                if event.key == pygame.K_RIGHT:
                    snake_update("right")
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if not snake_alive and (True in mouse_presses):
                    reset()

        screen.fill("#000000")

        screen.blit(infoZone, (0, 0))
        infoZone.fill("#dddddd")
        screen.blit(playZone, (0, 1.5*TILE_LENGTH))

        game_update()

        pygame.draw.rect(infoZone, "#ff3333", pygame.Rect(10, 0.25*TILE_LENGTH, TILE_LENGTH, TILE_LENGTH))
        infoZone.blit(font.render(str(snake_length), True, "#000000"), (50, 0.25*TILE_LENGTH))
        pygame.draw.rect(infoZone, "#ffff33", pygame.Rect(100, 0.25 * TILE_LENGTH, TILE_LENGTH, TILE_LENGTH))
        infoZone.blit(font.render(str(high_score), True, "#000000"), (160, 0.25 * TILE_LENGTH))

        clock.tick(12)
        pygame.display.flip()
