import pygame
import time
from BackEnd.SnakeClass import Snake


FPS = 60
VELOCITY = 0.3


pygame.init()
sc = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0001)')
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

sn = Snake([(i, 0) for i in range(15, -1, -1)], VELOCITY)

last_dir = None
running = True
clock = pygame.time.Clock()
while running:
	# event capture
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key in ck.keys():
				controls[ck[event.key]] = 1
		elif event.type == pygame.KEYUP:
			if event.key in ck.keys():
				controls[ck[event.key]] = 0
		elif event.type == pygame.WINDOWRESIZED:
			pygame.display.update()

	# moving snake if needed
	if any(controls):
		dir = controls.index(1)
		print(dir)
		if (not (last_dir == 0 and dir == 2)) and (not (dir == 0 and last_dir == 2)) and (not (last_dir == 1 and dir == 3)) and (not (dir == 1 and last_dir == 3)):
			last_dir = dir

	if last_dir is not None:
		sn.move(last_dir)
		cords2Draw = sn.listOfCoords_H2T()
		width, height = sc.get_size()
		print(cords2Draw, sc.get_size())
		sc.fill((0, 0, 0))
		for i in cords2Draw:
			pygame.draw.rect(sc, 'red', (i[0] / 40 * width, i[1] / 40 * height, 1 / 40 * width, 1 / 40 * height))

	pygame.display.update()
	clock.tick(FPS)
pygame.quit()
