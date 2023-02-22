import pygame
import time
from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field

FPS = 200
VELOCITY = 1
WALKEVERY = 10

pygame.init()
sc = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0004)')
pygame.display.set_icon(pygame.image.load('icon.png'))

executing = True
cnt = 1
controls = []
last_dir = 0
ck = {pygame.K_RIGHT: 0,
      pygame.K_d: 0,
      pygame.K_DOWN: 1,
      pygame.K_s: 1,
      pygame.K_LEFT: 2,
      pygame.K_a: 2,
      pygame.K_UP: 3,
      pygame.K_w: 3}

sn = Snake([(i, 0) for i in range(15, -1, -1)], VELOCITY)
sn2 = Snake([(i, 5) for i in range(4, -1, -1)], VELOCITY)

field = Field([sn, sn2], [0, 0])

running = True
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
            pygame.display.update()

    # moving snake if needed
    if cnt == 0:
        for sn_ind in range(2):
            cur = True
            for i in controls[::-1]:
                if field.move_snake(sn_ind, i):
                    last_dir = i
                    cur = False
                    break
            if cur: field.move_snake(sn_ind, last_dir)

        width, height = sc.get_size()
        sc.fill((0, 0, 0))
        for sn_ind in range(2):
            cords2Draw = field.snakes[sn_ind].listOfCoords_H2T()
            for i in cords2Draw:
                pygame.draw.rect(sc, 'green', (i[0] / 40 * width, i[1] / 40 * height, 1 / 40 * width, 1 / 40 * height))
            pygame.draw.rect(sc, 'red',
                             (field.apple[0] / 40 * width, field.apple[1] / 40 * height, 1 / 40 * width, 1 / 40 * height))

        pygame.display.update()
    clock.tick(FPS)
    cnt += 1
    cnt %= WALKEVERY
pygame.quit()
