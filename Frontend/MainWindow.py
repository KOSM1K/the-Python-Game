import pygame
from math import ceil

from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
from network import Network
import config

FPS = 200
WALKEVERY = 10
FIELD_SIZE = 40


def main():
	n = Network()
	self_id = n.player_id

	pygame.init()
	screen = pygame.display.set_mode((800, 800), (pygame.RESIZABLE if config.IS_RESIZABLE else 0))
	pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0004)')
	pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

	field = Field([], [], (FIELD_SIZE, FIELD_SIZE))
	sn = Snake([(i, 0) for i in range(15, -1, -1)], 0, config.VELOCITY, self_id, "green")
	field.appendSnake(sn, 0)
	data = n.send({"cords": field.snakes[self_id][0].coordinates, "apple": field.apple})
	print(data)
	room_id = data["room_id"]
	print("ROOM ID:", room_id)

	if data["apple"] is not None:
		field.apple = data["apple"]

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

			snake = field.snakes[self_id][0]

			if field.apple_changed_pos:
				field.apple_changed_pos = False
				apple = field.apple
			else:
				apple = None
			response_data = n.send({"cords": snake.coordinates, "dir": snake.dir, "apple": apple})

			field.apple = tuple(response_data["apple"])

			players_data = response_data["data"]
			snakes = list(map(lambda t: t["player_id"], players_data))

			for player in players_data:
				player_id = player["player_id"]
				if player_id not in field.snakes.keys():
					field.appendSnake(Snake(player["cords"], player["dir"], config.VELOCITY, player_id), player["dir"])
				else:
					field.update_cords(player_id, player["cords"], player["dir"])
					if field.snakes[player_id][0].find_crossover() != -1:
						if player_id == self_id:
							running = False
						else:
							del field.snakes[player_id]

			field_snakes = list(field.snakes.keys())
			for player_id in field_snakes:
				if player_id not in snakes:
					del field.snakes[player_id]
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
		snake = field.snakes[snake_id][0]
		cords2Draw = snake.listOfCoords_H2T()
		for i in cords2Draw:
			pygame.draw.rect(playingField, 'green' if snake_id == self_id else 'yellow',
							 (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
							  ceil(1 / fieldH * height)))
	pygame.draw.rect(playingField, 'red',
					 (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
					  1 / fieldH * height))

	screen.blit(playingField, (5, 5))
	pygame.display.update()
