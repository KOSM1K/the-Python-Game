import pygame
from math import ceil

from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
from network import Network
import config

FPS = 125
VELOCITY = 1
WALKEVERY = 10
FIELD_SIZE = 40


def main():
	n = Network()
	snake_id = n.id

	pygame.init()
	screen = pygame.display.set_mode((800, 800), (pygame.RESIZABLE if config.IS_RESIZABLE else 0))
	pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0004)')
	pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

	field = Field(snake_id, [], [], (FIELD_SIZE, FIELD_SIZE))
	sn = Snake(snake_id, [(i, 0) for i in range(15, -1, -1)], VELOCITY)
	field.appendSnake(sn, 0)

	n.send({"cords": sn.coordinates})

	snakes_len = len(field.snakes)

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
			cur = True
			for i in n.send({"controls": controls[::-1]})["controls"]:
				field.change_dir(snake_id, i)
				if field.move_snake(snake_id, i):
					cur = False
					break
			field.update()
			if cur: field.move_snake(snake_id, field.dirs[snake_id])
			if field.snakes[snake_id].find_crossover() != -1:
				running = False

			draw_field(field, screen, playingField)
		clock.tick(FPS)
		cnt += 1
		cnt %= WALKEVERY
	pygame.quit()


def resizePrepare(field: Field, screen):
	width, height = screen.get_size()
	size = min(width, height)
	playingField = pygame.Surface((size - 10, size - 10))
	pygame.draw.rect(screen, 'cyan',
					 (0, 0, size, size))
	draw_field(field, screen, playingField)
	return playingField


def draw_field(field: Field, screen, playingField):
	width, height = playingField.get_size()
	fieldW, fieldH = field.size
	playingField.fill((0, 0, 0))
	for snake_id, _ in field.snakes.items():
		cords2Draw = field.snakes[snake_id].listOfCoords_H2T()
		for i in cords2Draw:
			pygame.draw.rect(playingField, field.snakes[snake_id].color,
							 (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
							  ceil(1 / fieldH * height)))
	pygame.draw.rect(playingField, 'red',
					 (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
					  1 / fieldH * height))

	screen.blit(playingField, (5, 5))
	pygame.display.update()
