import pygame

from Frontend.LocalGameClass import LocalGame
from Frontend.EventHandlerClass import EventHandler


class MainWindow():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((610, 610), pygame.RESIZABLE)
        self.EvHndl = EventHandler()
        pygame.display.set_caption('the Python Game')
        pygame.display.set_icon(pygame.image.load('Frontend/Textures/icon.png'))

    def run(self):
        localGame = LocalGame(self.EvHndl, self.screen)
        localGame.run()


