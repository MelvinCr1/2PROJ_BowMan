import socket
import threading
import pickle
from gameState import GameState

class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.clients = []
        self.state = GameState()
        self.running = True

    def broadcast(self, data):
        for client in self.clients:
            try:
                client.sendall(pickle.dumps(data))
            except Exception as e:
                print(f"Erreur lors de l'envoi aux clients: {e}")

    def handle_client(self, client_socket, player_id):
        while self.running:
            try:
                data = client_socket.recv(4096)
                if data:
                    command = pickle.loads(data)
                    action = command.get("action")
                    if action == "tirer":
                        # Logique pour gérer un tir de flèche
                        self.state.add_arrow({"player": player_id, "position": (0, 0)})  # Exemples de valeurs
                    elif action == "quitter":
                        self.state.remove_player(player_id)
                        self.clients.remove(client_socket)
                        client_socket.close()
                        break

                    # Mise à jour globale du jeu
                    self.state.update()
                    self.broadcast(self.state)
                else:
                    break
            except Exception as e:
                print(f"Erreur lors de la gestion du client: {e}")
                break

        client_socket.close()

    def run(self):
        print("Le serveur est en cours d'exécution...")
        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f"Nouvelle connexion de {addr}")
            player_id = len(self.clients)
            self.state.add_player(player_id)
            self.clients.append(client_socket)

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, player_id))
            client_thread.start()

    def close(self):
        self.server_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 12345
    server = Server(host, port)
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()
