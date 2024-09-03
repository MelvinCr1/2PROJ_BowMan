import pygame
import sys
import os
import webbrowser
from creditsScene import CreditsScene

class OptionsScene:
    def __init__(self, screen, music_enabled=False, background_music=None):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets et docs depuis le répertoire principal
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')
        self.docs_path = os.path.join(self.base_path, '../docs/')

        # image de fond
        self.background_img = pygame.image.load(os.path.join(self.assets_path, 'backgrounds/background1.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

        # images des boutons
        self.music_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/music.png')).convert_alpha()
        self.audio_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/audio.png')).convert_alpha()
        self.questionmark_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/questionmark.png')).convert_alpha()
        self.info_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/info.png')).convert_alpha()

        # images alternatives des boutons
        self.audio_button_img_red = pygame.image.load(os.path.join(self.assets_path, 'buttons/audio_red.png')).convert_alpha()
        self.music_button_img_red = pygame.image.load(os.path.join(self.assets_path, 'buttons/music_red.png')).convert_alpha()

        # Redimensionner les images des boutons
        button_scale = 0.5
        self.music_button_img = pygame.transform.scale(self.music_button_img, (int(self.music_button_img.get_width() * button_scale), int(self.music_button_img.get_height() * button_scale)))
        self.audio_button_img = pygame.transform.scale(self.audio_button_img, (int(self.audio_button_img.get_width() * button_scale), int(self.audio_button_img.get_height() * button_scale)))
        self.questionmark_button_img = pygame.transform.scale(self.questionmark_button_img, (int(self.questionmark_button_img.get_width() * button_scale), int(self.questionmark_button_img.get_height() * button_scale)))
        self.info_button_img = pygame.transform.scale(self.info_button_img, (int(self.info_button_img.get_width() * button_scale), int(self.info_button_img.get_height() * button_scale)))
        self.audio_button_img_red = pygame.transform.scale(self.audio_button_img_red, (int(self.audio_button_img_red.get_width() * button_scale), int(self.audio_button_img_red.get_height() * button_scale)))
        self.music_button_img_red = pygame.transform.scale(self.music_button_img_red, (int(self.music_button_img_red.get_width() * button_scale), int(self.music_button_img_red.get_height() * button_scale)))

        # bouton "Retour"
        self.back_button_img = pygame.image.load(os.path.join(self.assets_path, 'buttons/back.png')).convert_alpha()
        self.back_button_img = pygame.transform.scale(self.back_button_img, (50, 50))
        self.back_button_rect = self.back_button_img.get_rect(topleft=(10, 10))  # Position en haut à gauche

        # rectangles de collision pour chaque bouton
        button_width, button_height = self.music_button_img.get_size()
        button_spacing = 20  # Espacement vertical entre les boutons
        total_height = button_height * 4 + button_spacing * 3  # Hauteur totale occupée par les boutons

        start_y = (self.height - total_height) // 2  # Position verticale de départ pour centrer les boutons

        self.music_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y, button_width, button_height)
        self.audio_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + (button_height + button_spacing), button_width, button_height)
        self.questionmark_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height)
        self.info_button_rect = pygame.Rect(self.width // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height)

        # Attributs d'état pour les boutons
        self.audio_active = False
        self.music_active = music_enabled

        # Initialisation de la musique de fond si activée
        if self.music_active and background_music:
            self.background_music = background_music
            self.background_music.play(-1)  # Jouer la musique en boucle
        else:
            self.background_music = None

    def run(self):
        running = True

        while running:
            self.screen.blit(self.background_img, (0, 0))

            # boutons en fonction de leur état
            if self.audio_active:
                self.screen.blit(self.audio_button_img_red, self.audio_button_rect)
            else:
                self.screen.blit(self.audio_button_img, self.audio_button_rect)

            if self.music_active:
                self.screen.blit(self.music_button_img_red, self.music_button_rect)
            else:
                self.screen.blit(self.music_button_img, self.music_button_rect)

            self.screen.blit(self.questionmark_button_img, self.questionmark_button_rect)
            self.screen.blit(self.info_button_img, self.info_button_rect)
            self.screen.blit(self.back_button_img, self.back_button_rect)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.back_button_rect.collidepoint(pos):
                            return
                        elif self.audio_button_rect.collidepoint(pos):
                            print("Gestion de l'audio...")
                            self.audio_active = not self.audio_active  # Inversement de l'état du bouton audio
                            # Implémentez la gestion de l'audio (à faire)
                        elif self.music_button_rect.collidepoint(pos):
                            print("Gestion de la musique...")
                            self.music_active = not self.music_active  # Inversement de l'état du bouton musique
                            if self.music_active and self.background_music:
                                self.background_music.play(-1)  # Jouer la musique en boucle
                            else:
                                pygame.mixer.music.stop()  # Arrêter la musique
                        elif self.questionmark_button_rect.collidepoint(pos):
                            print("Redirection vers la documentation utilisateur...")
                            pdf_path = os.path.join(self.docs_path, 'documentation_utilisateur.pdf')
                            if os.path.isfile(pdf_path):
                                webbrowser.open(pdf_path)  # Ouvrir le fichier PDF dans le navigateur
                            else:
                                print("Le fichier PDF n'existe pas.")
                        elif self.info_button_rect.collidepoint(pos):
                            credits_menu = CreditsScene(self.screen)
                            credits_menu.run()

            pygame.display.flip()
            self.clock.tick(30)