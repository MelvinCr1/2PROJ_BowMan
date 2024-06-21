import pygame
import sys

class EndGameMenu:
    def __init__(self, screen, winner):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.winner = winner  # Qui est le gagnant

        # Définir les couleurs
        self.background_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)

        # Charger les polices
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)

        # Définir les boutons
        self.play_again_button = pygame.Rect(self.width // 2 - 100, self.height // 2, 200, 50)
        self.quit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 70, 200, 50)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def run(self):
        running = True

        while running:
            self.screen.fill(self.background_color)

            # Afficher le texte du gagnant
            self.draw_text(f"{self.winner} a gagné!", self.font, self.text_color, self.screen, self.width // 2, self.height // 2 - 100)

            # Dessiner les boutons
            pygame.draw.rect(self.screen, self.button_color, self.play_again_button)
            pygame.draw.rect(self.screen, self.button_color, self.quit_button)

            # Texte des boutons
            self.draw_text("Rejouer", self.button_font, self.text_color, self.screen, self.play_again_button.centerx, self.play_again_button.centery)
            self.draw_text("Quitter", self.button_font, self.text_color, self.screen, self.quit_button.centerx, self.quit_button.centery)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pos = pygame.mouse.get_pos()
                        if self.play_again_button.collidepoint(pos):
                            from mainMenu import MainMenu
                            main_menu = MainMenu(self.screen)
                            main_menu.run()
                        elif self.quit_button.collidepoint(pos):
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man - Fin de partie')

    end_game_menu = EndGameMenu(screen, "Archer Gauche")
    end_game_menu.run()
