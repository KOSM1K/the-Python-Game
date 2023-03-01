import json
import socket
from _thread import *
import sys

from BackEnd.SnakeClass import Snake
import config


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((config.HOST, config.PORT))
except socket.error as e:
	print(e)


class Room:
	def __init__(self, max_players=5):
		self.max_players = max_players
		self.players: list[Snake] = list()
		self.apple = None

	def add_player(self, player: Snake):
		self.players.append(player)

	def get_player_index(self, player_id):
		return self.players_id.index(player_id)

	def remove_player(self, player_id):
		try:
			self.players.pop(self.get_player_index(player_id))
		except IndexError:
			pass

	def players_data(self):
		data = list()
		for snake in self.players:
			data.append({"player_id": snake.id, "snake_color": snake.color, "cords": snake.coordinates, "dir": snake.dir})
		return data

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
				room.add_player(Snake(cords, 0, config.VELOCITY, player_id))
				return room_id
		if len(self.rooms.keys()) == 0:
			last_id = 0
		else:
			last_id = max(self.rooms.keys()) + 1
		self.rooms[last_id] = Room()
		self.rooms[last_id].add_player(Snake(cords, 0, config.VELOCITY, player_id))
		return last_id

	def remove_player(self, player_id):
		for _, room in self.rooms.items():
			if player_id in room.players_id:
				room.remove_player(player_id)


rooms = Rooms()


s.listen(2)
print("Waiting for a connection, Server started!")


def read(conn):
	data = conn.recv(config.RECV_BYTES)
	return json.loads(data.decode("utf-8"))


def send(conn, data):
	conn.send_get(str.encode(json.dumps(data)))


def threaded_client(conn, addr):
	print("New thread!")
	player_id = addr[1]
	send(conn, {"player_id": player_id})

	data = read(conn)
	room_id = rooms.add_player(data["cords"], player_id)
	room = rooms.rooms[room_id]
	print("ROOM ID:", room_id)
	if rooms.rooms[room_id].apple is None:
		rooms.rooms[room_id].apple = data["apple"]
	send(conn, {"room_id": room_id, "data": rooms.rooms[room_id].players_data(), "apple": rooms.rooms[room_id].apple})

	while True:
		try:
			data = conn.recv(config.RECV_BYTES)
			if not data:
				break
			else:
				reply = json.loads(data.decode("utf-8"))
				print(reply)
				snake = room.players[room.get_player_index(player_id)]
				snake.coordinates = reply["cords"]
				snake.dir = reply["dir"]
				if reply["apple"] is not None:
					rooms.rooms[room_id].apple = reply["apple"]

				players_data = room.players_data()
				print({"apple": rooms.rooms[room_id].apple})
				send(conn, {"data": players_data, "apple": rooms.rooms[room_id].apple})
		except ConnectionResetError:
			break
	print("Disconnected")
	rooms.remove_player(player_id)
	conn.close()


while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, addr,))
