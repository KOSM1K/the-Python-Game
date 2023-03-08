import pygame
from math import ceil

from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
from BackEnd.EventHandlerClass import EventHandler

from network import Network
import config

FPS = 200
WALKEVERY = 10
FIELD_SIZE = 40
WINDOW_SIZE = (800, 800)


def main():
    n = Network()
    self_id = n.player_id

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, (pygame.RESIZABLE if config.IS_RESIZABLE else 0))
    pygame.display.set_caption('the Python Game (v1.0.0) (alpha 0005)')
    pygame.display.set_icon(pygame.image.load('Frontend/icon.png'))

    field = Field([], [], (FIELD_SIZE, FIELD_SIZE))

    cords = [(i, 0) for i in range(15, -1, -1)]
    sn = Snake([(i, 0) for i in range(15, -1, -1)], config.VELOCITY, 0, self_id, "green")
    field.appendSnake(sn)
    data = n.send_get({"cords": cords})
    print(data)

    room_id = data["room_id"]
    print("ROOM ID:", room_id)

    field.apple = tuple(data["apple"])

    playingField = resizePrepare(field, screen, self_id)

    running = True
    cnt = 1
    controls = []
    ck = {pygame.K_RIGHT: 0,
          pygame.K_d: 0,
          pygame.K_DOWN: 1,
          pygame.K_s: 1,
          pygame.K_LEFT: 2,
          pygame.K_a: 2,
          pygame.K_UP: 3,
          pygame.K_w: 3}

    clock = pygame.time.Clock()

    ev = EventHandler()

    while running:
        # event capture
        for event in pygame.event.get():
            ev.analyseEvent(event)
            running = not ev.events['quit']
            controls = ev.events['controls'][::-1]
            if ev.events['resize']:
                playingField = resizePrepare(field, screen, self_id)
                ev.events['resize'] = False

        # moving snake if needed
        if cnt == 0:
            if len(controls) != 0:
                field.change_dir(self_id, controls[0])
                web_clock(n, field, self_id, controls[0])
                # controls.pop(0)
            else:
                web_clock(n, field, self_id, None)

            # print(field.snakes[self_id].coordinates)
            # field.update(self_id=self_id)

            if field.snakes[self_id].find_crossover() != -1:
                running = False

            draw_field(field, screen, playingField, self_id)

        clock.tick(FPS)
        cnt += 1
        cnt %= WALKEVERY
    pygame.quit()


def resizePrepare(field: Field, screen, self_id):
    width, height = screen.get_size()
    size = min(width, height)
    playingField = pygame.Surface((size - 10, size - 10))
    pygame.draw.rect(screen, 'cyan',
                     (0, 0, size, size))
    draw_field(field, screen, playingField, self_id)
    return playingField


def draw_field(field: Field, screen, playingField, self_id):
    width, height = playingField.get_size()
    fieldW, fieldH = field.size
    playingField.fill((0, 0, 0))
    for snake_id in sorted(field.snakes.keys(), reverse=True, key=lambda x: abs(x - self_id)):
        cords2Draw = field.snakes[snake_id].listOfCoords_H2T()
        for i in cords2Draw:
            pygame.draw.rect(playingField, field.snakes[snake_id].color,
                             (i[0] / fieldW * width, i[1] / fieldH * height, ceil(1 / fieldW * width),
                              ceil(1 / fieldH * height)))
    pygame.draw.rect(playingField, 'red',
                     (field.apple[0] / fieldW * width, field.apple[1] / fieldH * height, 1 / fieldW * width,
                      1 / fieldH * height))

    screen.blit(playingField, (5, 5))
    pygame.display.update()


def web_clock(network: Network, field: Field, self_id: int, control: int):
    response_data = network.send_get({"control": control})
    field.apple = tuple(response_data["apple"])

    players_data = response_data["data"]
    snakes = list(map(lambda t: t["player_id"], players_data))

    for player in players_data:
        player_id = player["player_id"]
        if player_id not in field.snakes.keys():
            field.appendSnake(Snake(player["cords"], config.VELOCITY, player["dir"], player_id))
        else:
            field.snakes[player_id].coordinates = player["cords"]
            field.snakes[player_id].dir = player["dir"]
            field.snakes[player_id].HPointer = player["HPointer"]
            field.snakes[player_id].TPointer = player["TPointer"]
            if field.snakes[player_id].find_crossover() != -1:
                if player_id != self_id:
                    del field.snakes[player_id]

    field_snakes = list(field.snakes.keys())
    for player_id in field_snakes:
        if player_id not in snakes:
            del field.snakes[player_id]
