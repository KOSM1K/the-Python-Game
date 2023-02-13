class Snake:
    def __init__(self, coord: list[tuple], velocity):
        if len(coord) > 0:
            self.coordinates = coord
            self.HPointer = 0
            self.TPointer = len(coord) - 1
        else:
            raise ValueError("coordinates length must be at least 1")
        self.velocity = velocity

    def move(self, direction: int, incrLen: bool = False):
        '''
        :rtype: None
        :param direction: [0; 3] describes direction
        :type direction: int
        :param incrLen: default False. If true don't remove tail
        :type incrLen: bool
        Just moves the snake.
        '''

        dirs = [(self.velocity, 0), (0, self.velocity), (-self.velocity, 0), (0, -self.velocity)]

        if incrLen:
            self.coordinates.insert(self.HPointer,
                                    (self.coordinates[self.HPointer][0] + dirs[direction][0],
                                     self.coordinates[self.HPointer][1] + dirs[direction][1]))
            self.TPointer += int(self.HPointer < self.TPointer)
        else:
            NHPointer = (self.HPointer - 1) % len(self.coordinates)
            NTPointer = (self.TPointer - 1) % len(self.coordinates)
            self.coordinates[self.TPointer] = (self.coordinates[self.HPointer][0] + dirs[direction][0],
                                               self.coordinates[self.HPointer][1] + dirs[direction][1])
            self.HPointer = NHPointer
            self.TPointer = NTPointer

    def listOfCoords_H2T(self):
        '''
        makes a list of coordinates starting from head and ending at tail
        :return:
        '''
        lst = []
        for i in range(len(self.coordinates)):
            lst.append(self.coordinates[((self.HPointer + i) % len(self.coordinates))])
        return lst

    def predict(self, direction: int):
        dirs = [(self.velocity, 0), (0, self.velocity), (-self.velocity, 0), (0, -self.velocity)]
        return (self.coordinates[self.HPointer][0] + dirs[direction][0],
                self.coordinates[self.HPointer][1] + dirs[direction][1])
