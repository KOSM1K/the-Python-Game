import pygame
import time
from BackEnd.SnakeClass import Snake

pygame.init()
sc = pygame.display.set_mode((600, 300), pygame.RESIZABLE)
pygame.display.set_caption('the Python Game (v1.0.0)')
pygame.display.set_icon(pygame.image.load('icon.png'))

executing = True

controls = [0, 0, 0, 0]
ck = {pygame.K_RIGHT: 0,
      pygame.K_d: 0,
      pygame.K_DOWN: 1,
      pygame.K_s: 1,
      pygame.K_LEFT: 2,
      pygame.K_a: 2,
      pygame.K_UP: 3,
      pygame.K_w: 3}

sn = Snake([(i, 0) for i in range(3, -1, -1)])

while executing:
    pygame.draw.circle(sc, 'red', (250, 250), 50)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executing = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key in ck.keys():
                controls[ck[event.key]] = 1
        elif event.type == pygame.KEYUP:
            if event.key in ck.keys():
                controls[ck[event.key]] = 0
    if 1 in controls:
        dir = controls.index(1)
        sn.move(dir)
        print(sn.listOfCoords_H2T())
    time.sleep(0.5)
