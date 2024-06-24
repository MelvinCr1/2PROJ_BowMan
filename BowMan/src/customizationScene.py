import pygame
import sys
import os
from gameScene import GameScene

class CustomizationScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(base_path, '../assets/backgrounds/')  # Ajustez selon votre structure

        # Charger les images des backgrounds
        self.background_images = [
            pygame.image.load(os.path.join(self.assets_path, 'background1.jpg')).convert(),
            pygame.image.load(os.path.join(self.assets_path, 'background2.jpg')).convert(),
            pygame.image.load(os.path.join(self.assets_path, 'background3.jpg')).convert()
        ]

        # Redimensionner les images pour qu'elles remplissent l'écran
        self.background_images = [pygame.transform.scale(img, (self.width, self.height)) for img in self.background_images]

        # Index du fond sélectionné
        self.selected_background = 0

        # Définir les boutons de navigation
        self.prev_button = pygame.Rect(50, self.height // 2 - 25, 100, 50)
        self.next_button = pygame.Rect(self.width - 150, self.height // 2 - 25, 100, 50)
        self.start_button = pygame.Rect(self.width // 2 - 75, self.height - 100, 150, 50)

        # Polices
        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pos = pygame.mouse.get_pos()
                        if self.prev_button.collidepoint(pos):
                            self.selected_background = (self.selected_background - 1) % len(self.background_images)
                        elif self.next_button.collidepoint(pos):
                            self.selected_background = (self.selected_background + 1) % len(self.background_images)
                        elif self.start_button.collidepoint(pos):
                            game = GameScene(self.screen, self.background_images[self.selected_background])
                            game.run()

            self.screen.blit(self.background_images[self.selected_background], (0, 0))

            # Dessiner les boutons
            pygame.draw.rect(self.screen, (100, 100, 100), self.prev_button)
            pygame.draw.rect(self.screen, (100, 100, 100), self.next_button)
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_button)

            # Ajouter du texte aux boutons
            self.draw_text("Précédent", self.font, (255, 255, 255), self.screen, self.prev_button.centerx, self.prev_button.centery)
            self.draw_text("Suivant", self.font, (255, 255, 255), self.screen, self.next_button.centerx, self.next_button.centery)
            self.draw_text("Commencer", self.font, (255, 255, 255), self.screen, self.start_button.centerx, self.start_button.centery)

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man - Personnalisation')

    customization_menu = CustomizationScene(screen)
    customization_menu.run()
