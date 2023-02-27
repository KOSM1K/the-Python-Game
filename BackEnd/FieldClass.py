from BackEnd.SnakeClass import Snake
from random import randint


class Field:
	def __init__(self, snakes: list[Snake], dirs: list[int], size: tuple = (40, 40)):
		if len(snakes) == len(dirs):
			self.snakes: dict[int, list[Snake, int]] = {snakes[ind].id: [snakes[ind], dirs[ind]] for ind in range(len(snakes))}
			self.size = size
			self.apple = self.make_apple()
			self.apple_changed_pos = False
		else:
			raise ValueError("len(snakes) must be == len(dirs)")

	def move_snake(self, snake_id: int, dir: int):
		'''
		:param index: index of a snake
		:param dir: direction of moving
		:return:
		'''

		restr = {0: 2, 1: 3, 2: 0, 3: 1}
		if self.snakes[snake_id][1] != restr[dir]:
			self.snakes[snake_id][1] = dir
			self.snakes[snake_id][0].dir = dir

			apple_eat = ((self.snakes[snake_id][0].predict()[0] % self.size[0],
						 self.snakes[snake_id][0].predict()[1] % self.size[1]) == tuple(self.apple))
			self.snakes[snake_id][0].move(dir, apple_eat)
			self.snakes[snake_id][0].coordinates[self.snakes[snake_id][0].HPointer] = \
				(self.snakes[snake_id][0].coordinates[self.snakes[snake_id][0].HPointer][0] % self.size[0],
				 self.snakes[snake_id][0].coordinates[self.snakes[snake_id][0].HPointer][1] % self.size[1])

			if apple_eat:
				print("EAT:", (self.snakes[snake_id][0].coordinates[0][0] % self.size[0], self.snakes[snake_id][0].coordinates[0][1] % self.size[1]),
				      (self.snakes[snake_id][0].predict()[0] % self.size[0], self.snakes[snake_id][0].predict()[1] % self.size[1]),
				      self.apple)
				self.make_apple()

			return True
		else:
			return False

	def change_dir(self, snake_id, dir):
		restr = {0: 2, 1: 3, 2: 0, 3: 1}
		if self.snakes[snake_id][1] != restr[dir]:
			self.snakes[snake_id][1] = dir
			self.snakes[snake_id][0].dir = dir

	def update_cords(self, player_id, cords, dir):
		self.snakes[player_id][0].coordinates = cords
		self.snakes[player_id][0].dir, self.snakes[player_id][1] = dir, dir

	def update(self):
		for snake_id in self.snakes.keys():
			self.move_snake(snake_id, self.snakes[snake_id][1])

	def make_apple(self):
		c = True
		x, y = 0, 0
		while c:
			c = False
			x, y = randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)
			for i in self.snakes.keys():
				for j in self.snakes[i][0].coordinates:
					if (x, y) == j:
						c = True
						break
		self.apple = (x, y)
		self.apple_changed_pos = True
		return self.apple

	def appendSnake(self, sn: Snake, dir: int):
		self.snakes[sn.id] = [sn, dir]
