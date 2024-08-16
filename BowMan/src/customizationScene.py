import pygame
import os
import sys
from gameScene import GameScene

class CustomizationScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.selected_background = None
        self.selected_style = None
        self.play_mode = 'player vs player (local)'  # Valeur par défaut

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')

        self.background_options = ['background1.jpg', 'background2.jpg']
        self.style_options = ['archer.png', 'archer2.png']
        
        self.selected_background = self.background_options[0]
        self.selected_style = self.style_options[0]

        # Charger les images de fond et de style
        self.background_images = [self.load_image(os.path.join(self.assets_path, 'backgrounds', bg), (self.width, self.height)) for bg in self.background_options]
        self.style_images = [self.load_image(os.path.join(self.assets_path, 'characters', style), (200, 400)) for style in self.style_options]

        # Ajouter les modes de jeu possibles
        self.play_modes = ['player vs player (local)', 'player vs computer', 'multiplayer']
        self.current_mode_index = 0

        # Charger l'image du bouton "Retour"
        self.back_button_img = self.load_image(os.path.join(self.assets_path, 'buttons', 'back.png'), (50, 50))

        # Calculer la position et la zone cliquable de l'image du bouton
        self.back_button_rect = self.back_button_img.get_rect(topleft=(10, 10))

    def load_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return {"action": "main_menu"}
                elif event.key == pygame.K_RETURN:
                    return {"action": "start_game", "background": self.selected_background, "style": self.selected_style, "play_mode": self.play_mode}
                elif event.key == pygame.K_b:
                    current_index = self.background_options.index(self.selected_background)
                    self.selected_background = self.background_options[(current_index + 1) % len(self.background_options)]
                elif event.key == pygame.K_s:
                    current_index = self.style_options.index(self.selected_style)
                    self.selected_style = self.style_options[(current_index + 1) % len(self.style_options)]
                elif event.key == pygame.K_m:
                    # Changer le mode de jeu
                    self.current_mode_index = (self.current_mode_index + 1) % len(self.play_modes)
                    self.play_mode = self.play_modes[self.current_mode_index]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.back_button_rect.collidepoint(event.pos):
                        return {"action": "main_menu"}  # Retour au menu principal
        return None

    def draw(self):
        background_index = self.background_options.index(self.selected_background)
        self.screen.blit(self.background_images[background_index], (0, 0))

        style_index = self.style_options.index(self.selected_style)
        archer_left = self.style_images[style_index]
        archer_right = pygame.transform.flip(archer_left, True, False)

        left_position = (50, self.height // 2 - archer_left.get_height() // 2)
        right_position = (self.width - 250, self.height // 2 - archer_right.get_height() // 2)

        self.screen.blit(archer_left, left_position)
        self.screen.blit(archer_right, right_position)

        font = pygame.font.Font(None, 36)

        background_text = font.render(f"Background: {self.selected_background} (Press B to change)", True, (255, 255, 255))
        style_text = font.render(f"Style: {self.selected_style} (Press S to change)", True, (255, 255, 255))
        mode_text = font.render(f"Mode: {self.play_mode} (Press M to change)", True, (255, 255, 255))
        start_text = font.render("Press ENTER to start", True, (255, 255, 255))

        text_x = self.width // 2 - background_text.get_width() // 2
        base_y = self.height // 2 - 100
        self.screen.blit(background_text, (text_x, base_y))
        self.screen.blit(style_text, (text_x, base_y + 50))
        self.screen.blit(mode_text, (text_x, base_y + 100))
        self.screen.blit(start_text, (text_x, base_y + 150))

        self.screen.blit(self.back_button_img, self.back_button_rect.topleft)

        pygame.display.flip()

    def run(self):
        while True:
            result = self.handle_events()
            if result:
                if result["action"] == "start_game":
                    game = GameScene(self.screen, {
                        "background": result["background"],
                        "style": result["style"],
                        "play_mode": result["play_mode"]
                    })
                    game.run()
                if result["action"] == "main_menu":
                    return  # Retourne au menu principal en terminant la fonction `run`
            self.draw()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man')

    game = CustomizationScene(screen)
    settings = game.run()
