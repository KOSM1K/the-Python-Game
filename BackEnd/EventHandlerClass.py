import pygame


class EventHandler:
    def __init__(self):
        self.events = {'controls': [],
                       'quit': False,
                       'resize': False}

        self.controlKeys = {pygame.K_RIGHT: 0,
                            pygame.K_d: 0,
                            pygame.K_DOWN: 1,
                            pygame.K_s: 1,
                            pygame.K_LEFT: 2,
                            pygame.K_a: 2,
                            pygame.K_UP: 3,
                            pygame.K_w: 3}

    def analyseEvent(self, event: pygame.event.Event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            self.events['quit'] = True
        elif event.type == pygame.KEYDOWN:
            if event.key in self.controlKeys.keys():
                if self.controlKeys[event.key] not in self.events['controls']:
                    self.events['controls'].append(self.controlKeys[event.key])
        elif event.type == pygame.KEYUP:
            if event.key in self.controlKeys.keys():
                while self.controlKeys[event.key] in self.events['controls']:
                    self.events['controls'].remove(self.controlKeys[event.key])
        elif event.type == pygame.WINDOWRESIZED:
            self.events['resize'] = True
