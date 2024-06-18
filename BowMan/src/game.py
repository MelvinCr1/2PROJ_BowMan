import pygame
import sys
import os

# Définir quelques constantes utiles
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bow Man - Game')

# Charger les ressources
base_path = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(base_path, 'assets/')  # Assurez-vous d'ajuster selon votre structure de fichiers

# Charger l'image de fond
background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds/background.jpg')).convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Définir la boucle principale du jeu
def game():
    running = True

    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Affichage du fond
        screen.blit(background_img, (0, 0))

        # Actualiser l'écran
        pygame.display.flip()

        # Limiter la vitesse de rafraîchissement
        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__game__':
    game()
