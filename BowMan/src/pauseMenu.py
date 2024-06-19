# pauseMenu.py

import pygame
import sys
import os

from optionsMenu import OptionsMenu  # Importez votre classe OptionsMenu

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '../assets/')  # Ajustez selon votre structure

        # Charger les images des boutons et les redimensionner
        button_scale = 0.5  # Facteur d'échelle pour réduire la taille des boutons
        self.continue_button_img = pygame.image.load(os.path.join(assets_path, 'buttons/continue.png')).convert_alpha()
        self.continue_button_img = pygame.transform.scale(self.continue_button_img, (int(self.continue_button_img.get_width() * button_scale), int(self.continue_button_img.get_height() * button_scale)))

        self.options_button_img = pygame.image.load(os.path.join(assets_path, 'buttons/options.png')).convert_alpha()
        self.options_button_img = pygame.transform.scale(self.options_button_img, (int(self.options_button_img.get_width() * button_scale), int(self.options_button_img.get_height() * button_scale)))

        self.main_menu_button_img = pygame.image.load(os.path.join(assets_path, 'buttons/home.png')).convert_alpha()
        self.main_menu_button_img = pygame.transform.scale(self.main_menu_button_img, (int(self.main_menu_button_img.get_width() * button_scale), int(self.main_menu_button_img.get_height() * button_scale)))

        self.quit_button_img = pygame.image.load(os.path.join(assets_path, 'buttons/quit.png')).convert_alpha()
        self.quit_button_img = pygame.transform.scale(self.quit_button_img, (int(self.quit_button_img.get_width() * button_scale), int(self.quit_button_img.get_height() * button_scale)))

        # Positionner les boutons
        button_width, button_height = self.continue_button_img.get_size()
        button_spacing = 20  # Espacement vertical entre les boutons
        total_height = button_height * 4 + button_spacing * 3  # Hauteur totale occupée par les boutons

        start_y = (self.height - total_height) // 2  # Position verticale de départ pour centrer les boutons

        self.continue_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y, button_width, button_height)
        self.options_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + button_height + button_spacing, button_width, button_height)
        self.main_menu_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + (button_height + button_spacing) * 2, button_width, button_height)
        self.quit_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + (button_height + button_spacing) * 3, button_width, button_height)

    def draw(self):
        # Dessiner un fond semi-transparent
        s = pygame.Surface((self.width, self.height))  # Taille de l'écran
        s.set_alpha(128)  # Transparence (0-255)
        s.fill((0, 0, 0))  # Remplir de noir
        self.screen.blit(s, (0, 0))  # Dessiner sur l'écran

        # Dessiner les boutons
        self.screen.blit(self.continue_button_img, self.continue_button_rect)
        self.screen.blit(self.options_button_img, self.options_button_rect)
        self.screen.blit(self.main_menu_button_img, self.main_menu_button_rect)
        self.screen.blit(self.quit_button_img, self.quit_button_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    pos = pygame.mouse.get_pos()
                    if self.continue_button_rect.collidepoint(pos):
                        return "continue"
                    elif self.options_button_rect.collidepoint(pos):
                        options_menu = OptionsMenu(self.screen)  # Créer une instance du menu d'options
                        options_menu.run()
                    elif self.main_menu_button_rect.collidepoint(pos):
                        return "main_menu"
                    elif self.quit_button_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()
                        return "quit"
        return None
