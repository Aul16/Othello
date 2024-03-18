import pickle
import socket as sc

class Network:
    def __init__(self, server_ip="localhost"):   # To change if you want to play on a different server
        self.client = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.server = server_ip
        self.port = 5555             # Can be changed if the port is already used (server port must be changed too in server.py)
        self.addr = (self.server, self.port)

    def connect(self, gameId):
        try:
            self.client.connect(self.addr)
            self.send(gameId)
            return self.client.recv(2048).decode()  # Return the player number
        except sc.error:  # If the connection fails
            print("Connection failed")

    def send(self, data):
        self.client.send(str.encode(data))
        return pickle.loads(self.client.recv(2048))

    def disconnect(self):
        self.client.close()