from SnakeClass import Snake
from config import *

import time

class GameBackend:
    def __init__(self):
        field = ([], [], (FieldSizeX, FieldSizeY))
        snake = Snake([(i, 0) for i in range(15, -1, -1)], LenOfStep)
