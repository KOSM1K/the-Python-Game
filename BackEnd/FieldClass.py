from BackEnd.SnakeClass import Snake
from random import randint


class Field:
    def __init__(self, snakes: list[Snake], dirs: list[int], size: tuple = (40, 40)):
        if len(snakes) == len(dirs):
            self.size = size
            self.snakes = snakes
            self.dirs = dirs
            self.apple = None
            self.make_apple()
        else:
            raise ValueError("len(snakes) must be == len(dirs)")

    def move_snake(self, index: int, dir: int):
        '''

        :param index: index of a snake
        :param dir: direction of moving
        :return:
        '''
        restr = {0: 2, 1: 3, 2: 0, 3: 1}
        if self.dirs[index] != restr[dir]:
            self.dirs[index] = dir

            appl_eat = (self.snakes[index].predict(dir) == self.apple)
            self.snakes[index].move(dir, appl_eat)
            self.snakes[index].coordinates[self.snakes[index].HPointer] = \
                (self.snakes[index].coordinates[self.snakes[index].HPointer][0] % self.size[0],
                 self.snakes[index].coordinates[self.snakes[index].HPointer][1] % self.size[1])

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
