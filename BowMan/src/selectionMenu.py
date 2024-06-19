# backgroundSelectionMenu.py

import pygame
import sys
import os

class SelectionMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(base_path, '../assets/backgrounds/')  # Ajustez selon votre structure

        # Liste des noms de fichiers de fond disponibles
        self.background_options = ['background1.jpg', 'background2.jpg', 'background3.jpg']

        # Charger les images de fond et les redimensionner
        self.background_imgs = []
        for bg in self.background_options:
            img = pygame.image.load(os.path.join(self.assets_path, bg)).convert()
            img = pygame.transform.scale(img, (self.width // 3, self.height // len(self.background_options)))
            self.background_imgs.append(img)

        # Position des images de fond
        self.bg_rects = [img.get_rect(center=(self.width // 2, (self.height // len(self.background_options)) * (i + 1))) for i, img in enumerate(self.background_imgs)]
        self.selected_background = None

    def run(self):
        running = True

        while running:
            self.screen.fill((0, 0, 0))  # Remplir l'écran en noir

            # Afficher les options de fonds et les rectangles cliquables
            for i, img in enumerate(self.background_imgs):
                rect = img.get_rect(center=(self.width // 2, (self.height // len(self.background_options)) * (i + 1)))
                self.screen.blit(img, rect)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pos = pygame.mouse.get_pos()
                        for i, rect in enumerate(self.bg_rects):
                            if rect.collidepoint(pos):
                                self.selected_background = self.background_options[i]
                                running = False

            pygame.display.flip()
            self.clock.tick(30)  # Limiter la vitesse de rafraîchissement à 30 FPS

        return self.selected_background

    def select_background(self):
        return self.selected_background
