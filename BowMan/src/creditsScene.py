# creditsScene.py
import pygame
import sys
import os

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '../assets/')  # Ajustez selon votre structure

        # Charger l'image de fond pour la page de crédits
        self.background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds/background1.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

        # Charger la police pour le texte des crédits
        self.credits_font = pygame.font.Font(None, 36)  # Utilisez votre propre fichier de police si nécessaire

        # Texte des crédits
        self.credits_text = [
            "Bow Man Game",
            "Developed by Melvin C",
            "",
            "Credits:",
            "Sound Effects: //",
            "Background Music: Aberrant Realities",
            "Artwork: //",
            "",
            "© 2024 Melvin C. All Rights Reserved."
        ]

        # Calculer la position pour centrer le texte
        text_height = len(self.credits_text) * 36  # Hauteur totale du texte en pixels
        start_y = (self.height - text_height) // 2  # Position verticale de départ pour centrer le texte

        # Créer des surfaces de texte rendues avec la couleur noire (0, 0, 0)
        self.text_surfaces = []
        for line in self.credits_text:
            text_surface = self.credits_font.render(line, True, (0, 0, 0))
            text_width = text_surface.get_width()
            x = (self.width - text_width) // 2
            self.text_surfaces.append((text_surface, (x, start_y)))
            start_y += 36  # Espacement vertical entre les lignes de texte

        # Bouton retour au menu principal
        self.home_button_img = pygame.image.load(os.path.join(assets_path, 'buttons/back.png')).convert_alpha()
        button_scale = 0.5  # Facteur d'échelle pour réduire la taille du bouton
        self.home_button_img = pygame.transform.scale(self.home_button_img, (int(self.home_button_img.get_width() * button_scale), int(self.home_button_img.get_height() * button_scale)))
        button_width, button_height = self.home_button_img.get_size()
        self.home_button_rect = pygame.Rect(self.width // 2 - button_width // 2, self.height - button_height - 20, button_width, button_height)

    def run(self):
        running = True

        while running:
            self.screen.blit(self.background_img, (0, 0))  # Afficher le fond à l'arrière-plan

            # Afficher le texte des crédits
            for text_surface, (x, y) in self.text_surfaces:
                self.screen.blit(text_surface, (x, y))

            # Afficher le bouton retour au menu principal
            self.screen.blit(self.home_button_img, self.home_button_rect)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pos = pygame.mouse.get_pos()
                        if self.home_button_rect.collidepoint(pos):
                            return  # Retourner au menu des options

            pygame.display.flip()
            self.clock.tick(30)  # Limiter la vitesse de rafraîchissement à 30 FPS


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Bow Man')

    credits_page = CreditsScene(screen)
    credits_page.run()
