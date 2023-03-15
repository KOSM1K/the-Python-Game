from __future__ import annotations

import sys

import pygame
from math import ceil

from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
from BackEnd.EventHandlerClass import EventHandler

from network import Network
import config

FPS = 140
WALKEVERY = 10
FIELD_SIZE = 40
WINDOW_SIZE = (800, 800)


class Button:
	def __init__(self, text, pos, font, font_color="white", bg="black", pudding=5, pudding_left_right=None, action=None):
		self.x, self.y = pos
		self.action = action
		self.font_color = font_color
		self.bg = bg
		self.text = text

		self.x_pudding = pudding
		if pudding_left_right:
			self.x_pudding = pudding_left_right
		self.y_pudding = pudding

		self.font = pygame.font.SysFont("Verdana", font)
		self.size = None
		self.surface = None
		self.rect = None
		self.set_btn()

	def set_btn(self):
		self.text = self.font.render(self.text, True, pygame.Color(self.font_color))
		self.size = self.text.get_size()
		self.surface = pygame.Surface((self.size[0] + self.x_pudding * 2, self.size[1] + self.y_pudding * 2))
		self.surface.fill(self.bg)
		self.surface.blit(self.text, (self.x_pudding, self.y_pudding))
		self.rect = pygame.Rect(self.x - (self.size[0] // 2) - self.x_pudding, self.y - (self.size[1] // 2) - self.y_pudding,
		                        self.size[0] + self.x_pudding, self.size[1] + self.y_pudding)

	def show(self, screen):
		screen.blit(self.surface, (self.x - (self.size[0] // 2) - self.x_pudding, self.y - (self.size[1] // 2) - self.y_pudding))

	def is_clicked(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self.rect.collidepoint(x, y):
					if callable(self.action):
						self.action()
					return True
		return False


class ButtonsGroup:
	def __init__(self, buttons: list[Button] = None):
		if buttons is None:
			buttons = list()
		self.buttons = buttons

	def show(self, screen):
		for button in self.buttons:
			button.show(screen)

	def check_buttons(self, event):
		is_clicked = False
		for button in self.buttons:
			if button.is_clicked(event):
				is_clicked = True
		return is_clicked

	def add(self, button: Button):
		self.buttons.append(button)


def main():
	pygame.init()
	screen = pygame.display.set_mode(WINDOW_SIZE, (pygame.RESIZABLE if config.IS_RESIZABLE else 0))
	pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0005)')
	pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

	title_font = pygame.font.SysFont('Verdana', 80, bold=True)

	buttons = ButtonsGroup()
	buttons.add(Button("Single", (130, 450), 40, bg="#4aba2b", pudding=10, action=lambda: single_game_mode(screen)))
	buttons.add(Button("Multiplayer", (400, 450), 40, bg="#d1b22a", pudding=10, action=lambda: server_game_mode(screen)))
	buttons.add(Button("Exit", (670, 450), 40, bg="#c42f2f", pudding=10, action=lambda: sys.exit()))

	clock = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if buttons.check_buttons(event):
				break
			if event.type == pygame.QUIT:
				running = False

		screen.fill((0, 0, 0))

		title = title_font.render("Snake game", True, pygame.Color("green"))
		screen.blit(title, (400 - (title.get_width() // 2), 50))

		buttons.show(screen)
		pygame.display.update()
		clock.tick(FPS)
	pygame.quit()


def single_game_mode(screen: pygame.Surface | pygame.SurfaceType):
	self_id = 0

	field = Field([], [], (FIELD_SIZE, FIELD_SIZE))

	sn = Snake([(i, 0) for i in range(15, -1, -1)], config.VELOCITY, 0, self_id, "green")
	field.appendSnake(sn)

	playingField = resizePrepare(field, screen, self_id)

	running = True
	cnt = 1
	controls = []

	clock = pygame.time.Clock()

	ev = EventHandler()

	exit_btn = Button("x", (785, 15), 40, bg="#d12424", pudding=5)
	while running:
		# event capture
		for event in pygame.event.get():
			ev.analyseEvent(event)
			running = not ev.events['quit']
			controls = ev.events['controls'][::-1]
			if ev.events['resize']:
				playingField = resizePrepare(field, screen, self_id)
				ev.events['resize'] = False
			if exit_btn.is_clicked(event):
				running = False

		# moving snake if needed
		if cnt == 0:
			if len(controls) != 0:
				field.change_dir(self_id, controls[0])

			field.update()

			if field.snakes[self_id].find_crossover() != -1:
				running = False

			draw_field(field, screen, playingField, self_id)

		clock.tick(FPS)
		cnt += 1
		cnt %= WALKEVERY

		exit_btn.show(screen)
		pygame.display.update()


def server_game_mode(screen: pygame.Surface | pygame.SurfaceType):
	n = Network()
	self_id = n.player_id

	field = Field([], [], (FIELD_SIZE, FIELD_SIZE))

	cords = [(i, 0) for i in range(15, -1, -1)]
	sn = Snake([(i, 0) for i in range(15, -1, -1)], config.VELOCITY, 0, self_id, "green")
	field.appendSnake(sn)
	data = n.send_get({"cords": cords})
	print(data)

	room_id = data["room_id"]
	print("ROOM ID:", room_id)

	field.apple = tuple(data["apple"])

	playingField = resizePrepare(field, screen, self_id)

	running = True
	cnt = 1
	controls = []

	clock = pygame.time.Clock()

	ev = EventHandler()

	exit_btn = Button("x", (785, 15), 40, bg="#d12424", pudding=5)
	while running:
		# event capture
		for event in pygame.event.get():
			ev.analyseEvent(event)
			running = not ev.events['quit']
			controls = ev.events['controls'][::-1]
			if ev.events['resize']:
				playingField = resizePrepare(field, screen, self_id)
				ev.events['resize'] = False
			if exit_btn.is_clicked(event):
				running = False

		# moving snake if needed
		if cnt == 0:
			if len(controls) != 0:
				field.change_dir(self_id, controls[0])
				web_clock(n, field, self_id, controls[0])
			# controls.pop(0)
			else:
				web_clock(n, field, self_id)

			# print(field.snakes[self_id].coordinates)
			# field.update(self_id=self_id)

			if field.snakes[self_id].find_crossover() != -1:
				running = False

			draw_field(field, screen, playingField, self_id)

		clock.tick(FPS)
		cnt += 1
		cnt %= WALKEVERY

		exit_btn.show(screen)
		pygame.display.update()


def resizePrepare(field: Field, screen, self_id):
	width, height = screen.get_size()
	size = min(width, height)
	playingField = pygame.Surface((size - 10, size - 10))
	pygame.draw.rect(screen, 'cyan',
	                 (0, 0, size, size))
	draw_field(field, screen, playingField, self_id)
	return playingField


def draw_field(field: Field, screen, playingField, self_id):
	font = pygame.font.SysFont('Verdana', 15, bold=True)
	width, height = playingField.get_size()
	fieldW, fieldH = field.size
	playingField.fill((0, 0, 0))
	for snake_id in sorted(field.snakes.keys(), reverse=True, key=lambda x: abs(x - self_id)):
		cords2Draw = field.snakes[snake_id].listOfCoords_H2T()
		for index, i in enumerate(cords2Draw):
			color = pygame.Color(field.snakes[snake_id].color)
			hsla_color = color.hsla
			color.hsla = (hsla_color[0], hsla_color[1], hsla_color[2] - (0 if index == 0 else 7), hsla_color[3])

			pygame.draw.rect(playingField, color,
			                 (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
			                  ceil(1 / fieldH * height)))
		snake_name = font.render(field.snakes[snake_id].name, True, pygame.Color("white"))
		name_width, name_height = snake_name.get_size()
		playingField.blit(snake_name, ((cords2Draw[0][0] + 0.5) / fieldW * width - (name_width / 2),
		                               (cords2Draw[0][1] + 0.5) / fieldH * height - (name_height / 2)))

	pygame.draw.rect(playingField, 'red',
	                 (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
	                  1 / fieldH * height))

	screen.blit(playingField, (5, 5))


def web_clock(network: Network, field: Field, self_id: int, control: int = None):
	response_data = network.send_get({"control": control})
	field.apple = tuple(response_data["apple"])

	players_data = response_data["data"]
	snakes = list(map(lambda t: t["player_id"], players_data))

	for player in players_data:
		player_id = player["player_id"]
		if player_id not in field.snakes.keys():
			field.appendSnake(Snake(player["cords"], config.VELOCITY, player["dir"], player_id))
		else:
			field.snakes[player_id].coordinates = player["cords"]
			field.snakes[player_id].dir = player["dir"]
			field.snakes[player_id].HPointer = player["HPointer"]
			field.snakes[player_id].TPointer = player["TPointer"]
			if field.snakes[player_id].find_crossover() != -1:
				if player_id != self_id:
					del field.snakes[player_id]

	field_snakes = list(field.snakes.keys())
	for player_id in field_snakes:
		if player_id not in snakes:
			del field.snakes[player_id]
