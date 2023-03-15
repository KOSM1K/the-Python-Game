import socket
import json

import config


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = config.HOST
		self.port = config.PORT
		self.addr = (self.server, self.port)
		self.player_id = self.connect()["player_id"]
		print("PLAYER ID:", self.player_id)

	def connect(self):
		try:
			self.client.connect(self.addr)
			response = self.client.recv(config.RECV_BYTES).decode()[:-5]
			return json.loads(response)
		except:
			pass

	def send_get(self, data):
		try:
			self.client.send(str.encode(json.dumps(data)))
			response = b""
			while True:
				chunk = self.client.recv(config.RECV_BYTES)
				response += chunk
				if response.endswith(b"[END]"):
					break
			response = response.decode()[:-5]
			return json.loads(response)
		except socket.error as e:
			print(e)
