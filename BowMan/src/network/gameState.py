import math

class GameState:
    def __init__(self):
        self.players = {}  # joueurs connectés
        self.arrows = []  # liste des flèches en cours
        self.player_id = None  # identifiant unique du joueur local

    def add_player(self, player_id):
        self.players[player_id] = {"score": 0, "position": (0, 0), "alive": True, "health": 100}

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def update_position(self, player_id, position):
        if player_id in self.players:
            self.players[player_id]["position"] = position

    def add_arrow(self, arrow):
        self.arrows.append(arrow)

    def update(self):
        # Mettre à jour les flèches
        for arrow in self.arrows:
            if not arrow["active"]:
                continue

            # Mise à jour de la position de la flèche
            arrow["position"][0] += arrow["velocity"][0]
            arrow["position"][1] += arrow["velocity"][1]

            # Appliquer la gravité
            arrow["velocity"][1] += 0.5

            # Vérification des collisions avec les joueurs
            for player_id, player in self.players.items():
                if player["alive"] and self.check_collision(arrow, player):
                    player["health"] -= 10  # Dégâts infligés par une flèche
                    arrow["active"] = False  # La flèche ne doit plus être active après un impact
                    if player["health"] <= 0:
                        player["alive"] = False
                        print(f"Le joueur {player_id} a été éliminé.")
                    break

            # Vérification si la flèche sort de l'écran
            if self.is_arrow_out_of_bounds(arrow):
                arrow["active"] = False

        # Nettoyer les flèches inactives
        self.arrows = [arrow for arrow in self.arrows if arrow["active"]]

    def check_collision(self, arrow, player):
        arrow_x, arrow_y = arrow["position"]
        player_x, player_y = player["position"]

        if (player_x - 10 <= arrow_x <= player_x + 10) and (player_y - 10 <= arrow_y <= player_y + 10):
            return True
        return False

    def is_arrow_out_of_bounds(self, arrow):
        arrow_x, arrow_y = arrow["position"]
        if arrow_x < 0 or arrow_x > 800 or arrow_y > 600:
            return True
        return False
