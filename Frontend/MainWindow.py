import pygame
from math import ceil
from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field

FPS = 200
VELOCITY = 1
WALKEVERY = 10
FIELD_SIZE = 40


def main():
    pygame.init()
    screen = pygame.display.set_mode((810, 610), pygame.RESIZABLE)
    pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0004)')
    pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

    field = Field([], [], (FIELD_SIZE, FIELD_SIZE))
    sn = Snake([(i, 0) for i in range(15, -1, -1)], VELOCITY)
    field.appendSnake(sn, 0)
    NUM_OF_SNAKES = len(field.snakes)

    playingField = resizePrepare(field, screen)

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
                playingField = resizePrepare(field, screen)

        # moving snake if needed
        if cnt == 0:
            for sn_ind in range(NUM_OF_SNAKES):
                cur = True
                for i in controls[::-1]:
                    if field.move_snake(sn_ind, i):
                        cur = False
                        break
                if cur: field.move_snake(sn_ind, field.dirs[sn_ind])
                if field.snakes[sn_ind].find_crossover() != -1:
                    running = False

            draw_field(field, screen, playingField)
        clock.tick(FPS)
        cnt += 1
        cnt %= WALKEVERY
    pygame.quit()


def resizePrepare(field: Field, screen):
    width, height = screen.get_size()
    size = min(width - 200, height)
    playingField = pygame.Surface((size - 10, size - 10))
    pygame.draw.rect(screen, 'cyan',
                     (0, 0, size, size))
    draw_field(field, screen, playingField)
    return playingField


def draw_field(field: Field, screen, playingField):
    NUM_OF_SNAKES = len(field.snakes)
    width, height = playingField.get_size()
    fieldW, fieldH = field.size
    playingField.fill((0, 0, 0))
    for sn_ind in range(NUM_OF_SNAKES):
        cords2Draw = field.snakes[sn_ind].listOfCoords_H2T()
        for i in cords2Draw:
            pygame.draw.rect(playingField, 'green',
                             (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
                              ceil(1 / fieldH * height)))
    pygame.draw.rect(playingField, 'red',
                     (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
                      1 / fieldH * height))

    screen.blit(playingField, (5, 5))
    pygame.display.update()
