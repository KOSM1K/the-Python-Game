from BackEnd.SnakeClass import Snake
from random import randint


class Field:
	def __init__(self, snakes: list[Snake], dirs: list[int], size: tuple = (40, 40)):
		if len(snakes) == len(dirs):
			self.snakes: dict[int, Snake] = {snakes[ind].id: snakes[ind] for ind in range(len(snakes))}
			self.size = size
			self.apple = None
			self.make_apple()
			self.apple_changed_pos = False

		else:
			raise ValueError("len(snakes) must be == len(dirs)")

	def move_snake(self, snake_id: int, dir: int):
		'''
		:param snake_id:
		:param index: index of a snake
		:param dir: direction of moving
		:return:
		'''

		restr = {0: 2, 1: 3, 2: 0, 3: 1}
		if self.snakes[snake_id].dir != restr[dir]:
			self.snakes[snake_id].dir = dir

			appl_eat = ((self.snakes[snake_id].predict(dir)[0] % self.size[0],
						 self.snakes[snake_id].predict(dir)[1] % self.size[1]) == self.apple)
			self.snakes[snake_id].move(dir, appl_eat)
			self.snakes[snake_id].coordinates[self.snakes[snake_id].HPointer] = \
				(self.snakes[snake_id].coordinates[self.snakes[snake_id].HPointer][0] % self.size[0],
				 self.snakes[snake_id].coordinates[self.snakes[snake_id].HPointer][1] % self.size[1])

			if appl_eat:
				self.make_apple()

			return True
		else:
			return False

	def change_dir(self, snake_id, dir):
		restr = {0: 2, 1: 3, 2: 0, 3: 1}
		if self.snakes[snake_id].dir != restr[dir]:
			self.snakes[snake_id].dir = dir

	def update(self):
		for snake_id in self.snakes.keys():
			self.move_snake(snake_id, self.snakes[snake_id].dir)

	def make_apple(self):
		c = True
		x, y = 0, 0
		while c:
			c = False
			x, y = randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)
			for i in self.snakes.keys():
				for j in self.snakes[i].coordinates:
					if (x, y) == j:
						c = True
						break
		self.apple = (x, y)
		self.apple_changed_pos = True

	def appendSnake(self, sn: Snake):
		self.snakes[sn.id] = sn
