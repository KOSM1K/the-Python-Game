import json
import socket
from _thread import *
import sys

from BackEnd.SnakeClass import Snake
from BackEnd.FieldClass import Field
import config


class Room:
    def __init__(self, max_players=5):
        self.max_players: int = max_players
        self.field: Field = Field(list(), list())

    def add_player(self, player: Snake):
        self.field.appendSnake(player)

    def remove_player(self, player_id):
        try:
            del self.field.snakes[player_id]
        except IndexError:
            pass

    def players_data(self):
        data = list()
        for snake in self.players:
            data.append(
                {"player_id": snake.id, "snake_color": snake.color, "cords": snake.coordinates, "dir": snake.dir,
                 "HPointer": snake.HPointer, "TPointer": snake.TPointer})
        return data

    @property
    def players(self):
        return list(self.field.snakes.values())

    @property
    def is_free(self):
        return len(self.players) < self.max_players

    @property
    def players_id(self):
        return list(map(lambda t: t.id, self.players))


class Rooms:
    def __init__(self):
        self.rooms: dict[int, Room] = {}

    def add_player(self, cords, player_id):
        for room_id, room in self.rooms.items():
            if room.is_free:
                room.add_player(Snake(cords, config.VELOCITY, 0, player_id))
                return room_id
        if len(self.rooms.keys()) == 0:
            last_id = 0
        else:
            last_id = max(self.rooms.keys()) + 1
        self.rooms[last_id] = Room()
        self.rooms[last_id].add_player(Snake(cords, config.VELOCITY, 0, player_id))
        return last_id

    def remove_player(self, player_id):
        for _, room in self.rooms.items():
            if player_id in room.players_id:
                room.remove_player(player_id)


def read(conn):
    data = conn.recv(config.RECV_BYTES)
    return json.loads(data.decode("utf-8"))


def send(conn, data):
    conn.send(str.encode(json.dumps(data)))


def threaded_client(conn, addr):
    print("New thread!")
    player_id = addr[1]
    send(conn, {"player_id": player_id})

    data = read(conn)
    room_id = rooms.add_player(list(map(tuple, data["cords"])), player_id)
    room = rooms.rooms[room_id]
    print("ROOM ID:", room_id)

    send(conn, {"room_id": room_id, "data": room.players_data(), "apple": room.field.apple})

    while True:
        try:
            data = conn.recv(config.RECV_BYTES)
            if not data:
                break
            else:
                reply = json.loads(data.decode("utf-8"))
                # print(reply)

                if reply["control"] is not None:
                    room.field.change_dir(player_id, reply["control"])
                room.field.move_snake(player_id, room.field.snakes[player_id].dir)
                room.field.snakes[player_id].listOfCoords_H2T()

                players_data = room.players_data()
                # print({"apple": room.field.apple, "data": players_data})
                send(conn, {"data": players_data, "apple": room.field.apple})
        except ConnectionResetError:
            break
    print("Disconnected")
    rooms.remove_player(player_id)
    conn.close()


rooms = None


def server_init():
    global rooms
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((config.HOST, config.PORT))
    except socket.error as e:
        print(e)

    rooms = Rooms()

    s.listen(2)
    print("Waiting for a connection, Server started!")

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, addr,))
