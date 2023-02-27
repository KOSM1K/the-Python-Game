import pygame
from math import ceil

from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
from network import Network
import config

FPS = 200
VELOCITY = 1
WALKEVERY = 10
FIELD_SIZE = 40


def main():
    # n = Network()
    # self_id = n.id
    self_id = 0

    pygame.init()
    screen = pygame.display.set_mode((800, 800), (pygame.RESIZABLE if config.IS_RESIZABLE else 0))
    pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0004)')
    pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

    field = Field([], [], (FIELD_SIZE, FIELD_SIZE))
    sn = Snake([(i, 0) for i in range(15, -1, -1)], VELOCITY, self_id)
    sn2 = Snake([(i, 5) for i in range(15, -1, -1)], VELOCITY, 2)
    field.appendSnake(sn, 0)
    field.appendSnake(sn2, 0)

    playingField = resizePrepare(field, screen, self_id)

    running = True
    cnt = 1
    controls = []
    ck = {pygame.K_RIGHT: 0,
          pygame.K_d: 0,
          pygame.K_DOWN: 1,
          pygame.K_s: 1,
          pygame.K_LEFT: 2,
          pygame.K_a: 2,
          pygame.K_UP: 3,
          pygame.K_w: 3}

    clock = pygame.time.Clock()
    while running:
        # event capture
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in ck.keys():
                    if ck[event.key] not in controls:
                        controls.append(ck[event.key])
            elif event.type == pygame.KEYUP:
                if event.key in ck.keys():
                    controls.remove(ck[event.key])
            elif event.type == pygame.WINDOWRESIZED:
                playingField = resizePrepare(field, screen, self_id)

        # moving snake if needed
        if cnt == 0:
            cur = True
            for i in controls:
                field.change_dir(self_id, i)
                break
            field.update()
            if field.snakes[self_id][0].find_crossover() != -1:
                running = False

            draw_field(field, screen, playingField, self_id)
        clock.tick(FPS)
        cnt += 1
        cnt %= WALKEVERY
    pygame.quit()


def resizePrepare(field: Field, screen, self_id):
    width, height = screen.get_size()
    size = min(width, height)
    playingField = pygame.Surface((size - 10, size - 10))
    pygame.draw.rect(screen, 'cyan',
                     (0, 0, size, size))
    draw_field(field, screen, playingField, self_id)
    return playingField


def draw_field(field: Field, screen, playingField, self_id):
    width, height = playingField.get_size()
    fieldW, fieldH = field.size
    playingField.fill((0, 0, 0))
    for snake_id in field.snakes.keys():
        cords2Draw = field.snakes[snake_id][0].listOfCoords_H2T()
        for i in cords2Draw:
            pygame.draw.rect(playingField, 'green' if snake_id == self_id else 'yellow',
                             (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
                              ceil(1 / fieldH * height)))
    pygame.draw.rect(playingField, 'red',
                     (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
                      1 / fieldH * height))

    screen.blit(playingField, (5, 5))
    pygame.display.update()
