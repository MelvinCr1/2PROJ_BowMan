import socket
import threading
import pickle
from gameState import GameState

class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.state = GameState()
        self.running = True

    def send_data(self, data):
        try:
            self.client_socket.sendall(pickle.dumps(data))
        except Exception as e:
            print(f"Erreur lors de l'envoi des données: {e}")
            self.running = False

    def receive_data(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096)
                if data:
                    self.state = pickle.loads(data)
                else:
                    print("Connexion fermée par le serveur.")
                    self.running = False
            except Exception as e:
                print(f"Erreur lors de la réception des données: {e}")
                self.running = False

    def close(self):
        self.client_socket.close()

    def run(self):
        # Thread de réception des données
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

        # Main loop
        while self.running:
            command = input("Entrer une commande (tirer, quitter): ")
            if command == "tirer":
                # Simuler un tir et envoyer l'action au serveur
                self.send_data({"action": "tirer", "player": self.state.player_id})
            elif command == "quitter":
                self.send_data({"action": "quitter", "player": self.state.player_id})
                self.running = False

        self.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345
    client = Client(host, port)
    client.run()
