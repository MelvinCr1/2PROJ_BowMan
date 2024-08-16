import pygame
import sys
import os
from optionsScene import OptionsScene
from gameScene import GameScene
from customizationScene import CustomizationScene

class MainScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')

        # Charger l'image de fond
        self.background_img = pygame.image.load(os.path.join(self.assets_path, 'backgrounds/background1.jpg')).convert()

        # Redimensionner l'image de fond pour qu'elle remplisse l'écran
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

        # Chargement des images des boutons et les redimensionner
        button_scale = 0.5  # Facteur d'échelle pour réduire la taille des boutons
        self.play_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/play.png')).convert_alpha()
        self.play_button_img = pygame.transform.scale(self.play_button_img, (int(self.play_button_img.get_width() * button_scale), int(self.play_button_img.get_height() * button_scale)))

        self.options_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/options.png')).convert_alpha()
        self.options_button_img = pygame.transform.scale(self.options_button_img, (int(self.options_button_img.get_width() * button_scale), int(self.options_button_img.get_height() * button_scale)))

        self.quit_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/quit.png')).convert_alpha()
        self.quit_button_img = pygame.transform.scale(self.quit_button_img, (int(self.quit_button_img.get_width() * button_scale), int(self.quit_button_img.get_height() * button_scale)))

        # Positionner les boutons
        button_width, button_height = self.play_button_img.get_size()
        button_spacing = 20  # Espacement vertical entre les boutons
        total_height = button_height * 3 + button_spacing * 2  # Hauteur totale occupée par les boutons

        start_y = (self.height - total_height) // 2  # Position verticale de départ pour centrer les boutons

        self.play_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y, button_width, button_height)
        self.options_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + button_height + button_spacing, button_width, button_height)
        self.quit_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + (button_height + button_spacing) * 2, button_width, button_height)

        # Chemin vers le dossier assets/sounds
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')

    def run(self):
        pygame.mixer.init()
        background_music = pygame.mixer.Sound(os.path.join(self.assets_path, 'sounds/background_music.mp3'))
        background_music.play(loops=-1)  # -1 -> jouer en boucle indéfiniment

        running = True
        while running:
            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.play_button_img, self.play_button_rect)
            self.screen.blit(self.options_button_img, self.options_button_rect)
            self.screen.blit(self.quit_button_img, self.quit_button_rect)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Bouton gauche de la souris
                        pos = pygame.mouse.get_pos()
                        if self.play_button_rect.collidepoint(pos):
                            customization_scene = CustomizationScene(self.screen)
                            result = customization_scene.run()
                            if result is None or result.get('action') == 'main_menu':
                                continue
                            elif result.get('action') == 'start_game':
                                game_scene = GameScene(self.screen, result)
                                game_scene.run()
                        elif self.options_button_rect.collidepoint(pos):
                            options_menu = OptionsScene(self.screen, background_music=background_music)  # Création instance du menu d'options
                            options_menu.run()
                        elif self.quit_button_rect.collidepoint(pos):
                            print("Fermeture du jeu...")
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            self.clock.tick(30)  # Limiter la vitesse de rafraîchissement à 30 FPS

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man')

    menu = MainScene(screen)
    menu.run()
