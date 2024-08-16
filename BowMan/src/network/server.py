import socket
import threading
import pickle

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)  # Limité à deux joueurs pour ce jeu

        self.clients = []
        self.game_state = {
            'archer_left_pos': (50, 200),
            'archer_right_pos': (2350, 200),
            'arrows': []
        }

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                action_data = pickle.loads(data)
                self.update_game_state(action_data)
                self.broadcast_game_state()
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def update_game_state(self, action_data):
        # Mettre à jour l'état du jeu en fonction de l'action reçue
        self.game_state['arrows'].append(action_data)

    def broadcast_game_state(self):
        serialized_state = pickle.dumps(self.game_state)
        for client in self.clients:
            client.sendall(serialized_state)

    def run(self):
        print("Server is running...")
        while True:
            client_socket, _ = self.server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
