# game.py

import pygame
import sys
import os


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '../assets/')  # Ajustez selon votre structure

        # Définir les nouvelles dimensions de la fenêtre de jeu
        self.width, self.height = 1200, 800  # Agrandir la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Charger l'image de fond
        self.background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds/background.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

        # Charger l'image de l'archer
        self.archer_img = pygame.image.load(os.path.join(assets_path, 'characters/archer.png')).convert_alpha()
        self.archer_img = pygame.transform.scale(self.archer_img, (150, 300))  # Ajuster la taille de l'archer
        self.archer_img_left_rect = self.archer_img.get_rect(
            topleft=(50, self.height // 2 - self.archer_img.get_height() // 2))

        # Inverser l'image de l'archer pour la droite
        self.archer_img_right = pygame.transform.flip(self.archer_img, True, False)
        self.archer_img_right_rect = self.archer_img_right.get_rect(
            topright=(self.width - 50, self.height // 2 - self.archer_img_right.get_height() // 2))

    def run(self):
        running = True

        while running:
            self.screen.blit(self.background_img, (0, 0))  # Afficher le fond à l'arrière-plan

            # Afficher l'image de l'archer de chaque côté
            self.screen.blit(self.archer_img, self.archer_img_left_rect)
            self.screen.blit(self.archer_img_right, self.archer_img_right_rect)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pass  # Ajouter votre logique de jeu ici

            pygame.display.flip()
            self.clock.tick(30)  # Limiter la vitesse de rafraîchissement à 30 FPS


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))  # Agrandir la fenêtre
    pygame.display.set_caption('Bow Man - Jeu')

    game = Game(screen)
    game.run()
