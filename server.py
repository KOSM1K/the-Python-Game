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
		self.players = list()

	@property
	def is_free(self):
		return len(self.players) < self.max_players

	def add_player(self, player: Snake):
		self.players.append(player)


rooms = [Room()]


s.listen(2)
print("Waiting for a connection, Server started!")


def threaded_client(conn, addr):
	# for room in rooms:
	# 	if room.is_free:
	# 		room.add_player(Snake(addr[1]))
	conn.send(str.encode(json.dumps({"player_id": addr[1]})))
	reply = ""
	while True:
		try:
			data = conn.recv(2048)
			reply = json.loads(data.decode("utf-8"))

			if not data:
				print("Disconnected")
				break
			else:
				print(reply)
				for key, value in reply.items():
					pass
				conn.sendall(str.encode(reply))
		except:
			break


while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, addr,))
