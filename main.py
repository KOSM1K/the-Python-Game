from BackEnd.SnakeClass import Snake

if __name__ == '__main__':
    snTest = Snake([(i, 0) for i in range(3, -1, -1)])
    while True:
        print(snTest.HPointer, snTest.TPointer, snTest.listOfCoords_H2T())
        snTest.move(int(input()))
