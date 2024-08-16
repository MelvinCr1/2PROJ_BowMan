import socket
import threading
import pickle


class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_action(self, action_data):
        serialized_data = pickle.dumps(action_data)
        self.socket.sendall(serialized_data)

    def receive_game_state(self):
        serialized_state = self.socket.recv(4096)
        return pickle.loads(serialized_state)