import pygame
from math import ceil
from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
from BackEnd.EventHandlerClass import EventHandler


class MainWindow():
    def __init__(self):
        self.FontFillColor = (50, 50, 50)
        self.BorderColor = (100, 100, 100)

        self.SPS = 20  # steps per second
        self.FIELD_SIZE = 40  # length of side of square

        # DO NOT CHANGE!
        self.lenOfStep = 1  # length by one step


    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((610, 610), pygame.RESIZABLE)
        pygame.display.set_caption('the Python Game')
        pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

        self.field = Field([], [], (self.FIELD_SIZE, self.FIELD_SIZE))
        sn = Snake([(i, 0) for i in range(15, -1, -1)], self.lenOfStep)
        self.field.appendSnake(sn, 0)
        self.EvHndl = EventHandler()

        self.playingField = self.resizePrepare(self.field, self.screen)

        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                self.EvHndl.analyseEvent(event)
                if self.EvHndl.events['quit']:
                    running = False
                elif self.EvHndl.events['resize']:
                    playingField = self.resizePrepare(self.field, self.screen)

            # moving snake if needed
            for sn_ind in range(len(self.field.snakes)):
                for i in self.EvHndl.events['controls'][::-1] + [self.field.dirs[sn_ind]]:
                    if not self.field.move_snake(sn_ind, i):
                        pass
                    else:
                        break
                if self.field.snakes[sn_ind].find_crossover() != -1:
                    running = False

                self.draw_field(self.field, self.screen, self.playingField)
            clock.tick(self.SPS)
        pygame.quit()


    def resizePrepare(self, field: Field, screen):
        width, height = screen.get_size()
        size = min(width, height)
        playingField = pygame.Surface((size - 10, size - 10))
        pygame.draw.rect(screen, 'gray',
                         (0, 0, size, size))
        self.draw_field(field, screen, playingField)
        return playingField


    def draw_field(self, field: Field, screen, playingField):
        NUM_OF_SNAKES = len(field.snakes)
        width, height = playingField.get_size()
        fieldW, fieldH = field.size
        playingField.fill((0, 0, 0))
        for sn_ind in range(NUM_OF_SNAKES):
            cords2Draw = field.snakes[sn_ind].listOfCoords_H2T()
            for i in cords2Draw:
                pygame.draw.rect(playingField, 'green',
                                 (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
                                  ceil(1 / fieldH * height)))
        pygame.draw.rect(playingField, 'red',
                         (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
                          1 / fieldH * height))

        screen.blit(playingField, (5, 5))
        pygame.display.update()
