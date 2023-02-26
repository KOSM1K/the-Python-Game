from BackEnd.SnakeClass import Snake
from random import randint


class Field:
	def __init__(self, snakes: list[Snake], dirs: list[int], size: tuple = (40, 40)):
		if len(snakes) == len(dirs):
			self.size = size
			self.snakes = {t.snake_id: t for t in snakes}
			self.dirs = dirs
			self.apple = None
			self.make_apple()
		else:
			raise ValueError("len(snakes) must be == len(dirs)")

	def move_snake(self, snake_id: int, dir: int):
		'''
		:param index: index of a snake
		:param dir: direction of moving
		:return:
		'''
		print(self.snakes)

		restr = {0: 2, 1: 3, 2: 0, 3: 1}
		if self.dirs[snake_id] != restr[dir]:
			self.dirs[snake_id] = dir

			appl_eat = (self.snakes[snake_id].predict(dir) == self.apple)
			self.snakes[snake_id].move(dir, appl_eat)
			self.snakes[snake_id].coordinates[self.snakes[snake_id].HPointer] = \
				(self.snakes[snake_id].coordinates[self.snakes[snake_id].HPointer][0] % self.size[0],
				 self.snakes[snake_id].coordinates[self.snakes[snake_id].HPointer][1] % self.size[1])

			if appl_eat:
				self.make_apple()

			return True
		else:
			return False

	def make_apple(self):
		c = True
		x, y = 0, 0
		while c:
			c = False
			x, y = randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)
			for i in self.snakes:
				for j in i.coordinates:
					if (x, y) == j:
						c = True
						break
		self.apple = (x, y)

	def appendSnake(self, sn: Snake, dir:int):
		self.snakes.append(sn)
		self.dirs.append(dir)
