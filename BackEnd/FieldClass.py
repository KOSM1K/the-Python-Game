from BackEnd.SnakeClass import Snake


class Field:
    def __init__(self, snakes: list[Snake], dirs: list[int], size: tuple = (40, 40)):
        if len(snakes) == len(dirs):
            self.size = size
            self.snakes = snakes
            self.dirs = dirs
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

            self.snakes[index].move(dir)
            self.snakes[index].coordinates[self.snakes[index].HPointer] = \
                (self.snakes[index].coordinates[self.snakes[index].HPointer][0] % self.size[0],
                 self.snakes[index].coordinates[self.snakes[index].HPointer][1] % self.size[1])

            return True
        else:
            return False
