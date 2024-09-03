import pygame
import sys
import os

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')

        # Chargement image de fond
        self.background_img = pygame.image.load(os.path.join(self.assets_path, 'backgrounds/background1.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

        # Chargement police
        self.credits_font = pygame.font.Font(None, 36)

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

        text_height = len(self.credits_text) * 36  # Hauteur texte
        start_y = (self.height - text_height) // 2  # Position verticale texte

        self.text_surfaces = []
        for line in self.credits_text:
            text_surface = self.credits_font.render(line, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (self.width - text_width) // 2
            self.text_surfaces.append((text_surface, (x, start_y)))
            start_y += 36  # Espacement entre les lignes

        # Bouton "Retour"
        self.back_button_img = self.load_image(os.path.join(self.assets_path, 'buttons', 'back.png'), (50, 50))
        self.back_button_rect = self.back_button_img.get_rect(topleft=(10, 10))

    def load_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image

    def run(self):
        running = True

        while running:
            self.screen.blit(self.background_img, (0, 0)) 

            # Afficher le texte des crédits
            for text_surface, (x, y) in self.text_surfaces:
                self.screen.blit(text_surface, (x, y))

            # Afficher le bouton "Retour"
            self.screen.blit(self.back_button_img, self.back_button_rect.topleft)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pos = pygame.mouse.get_pos()
                        if self.back_button_rect.collidepoint(pos):
                            return

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Bow Man')

    credits_page = CreditsScene(screen)
    credits_page.run()
