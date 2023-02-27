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
            return json.loads(self.client.recv(config.RECV_BYTES).decode())
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(json.dumps(data)))
            return json.loads(self.client.recv(config.RECV_BYTES).decode())
        except socket.error as e:
            print(e)
