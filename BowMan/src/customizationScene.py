import pygame
import os
import sys
from gameScene import GameScene

class CustomizationScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Valeur par défaut
        self.selected_background = None
        self.selected_style = None
        self.obstacle_option = False
        self.play_mode = 'player vs player (local)'

        # Initialiser la case à cocher
        self.checkbox_rect = pygame.Rect(0, 0, 20, 20)  # Position initiale sera mise à jour
        self.checkbox_color = (255, 255, 255)
        self.tick_color = (0, 255, 0)  # Couleur du tick
        self.font = pygame.font.Font(None, 36)

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')

        self.background_options = ['background1.jpg', 'background2.jpg']
        self.style_options = ['archer.png', 'archer2.png']
        
        self.selected_background = self.background_options[0]
        self.selected_style = self.style_options[0]

        # Charger les images de fond
        self.background_images = [self.load_image(os.path.join(self.assets_path, 'backgrounds', bg), (self.width, self.height)) for bg in self.background_options]

        # Charger les images de style sans redimensionner
        self.style_images = [self.load_image(os.path.join(self.assets_path, 'characters', style), None) for style in self.style_options]

        # Ajouter les modes de jeu possibles
        self.play_modes = ['player vs player (local)', 'player vs computer', 'multiplayer']
        self.current_mode_index = 0

        # Dictionnaire de couleurs pour la tige de la flèche
        self.arrow_color_names = ['Rouge', 'Vert', 'Bleu', 'Jaune']
        self.arrow_colors = {
            'Rouge': (255, 0, 0),
            'Vert': (0, 255, 0),
            'Bleu': (0, 0, 255),
            'Jaune': (255, 255, 0)
        }
        self.selected_arrow_color_name = self.arrow_color_names[0]
        self.selected_arrow_color = self.arrow_colors[self.selected_arrow_color_name]

        # Charger l'image du bouton "Retour"
        self.back_button_img = self.load_image(os.path.join(self.assets_path, 'buttons', 'back.png'), (50, 50))

        # Calculer la position et la zone cliquable de l'image du bouton
        self.back_button_rect = self.back_button_img.get_rect(topleft=(10, 10))

    def load_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image

    def draw(self):
        # Dessiner l'arrière-plan
        background_index = self.background_options.index(self.selected_background)
        self.screen.blit(self.background_images[background_index], (0, 0))

        # Dessiner les archers avec le style sélectionné à leur taille originale
        style_index = self.style_options.index(self.selected_style)
        archer_left = self.style_images[style_index]
        archer_right = pygame.transform.flip(archer_left, True, False)

        left_position = (50, self.height // 2 - archer_left.get_height() // 2)
        right_position = (self.width - archer_right.get_width() - 50, self.height // 2 - archer_right.get_height() // 2)

        self.screen.blit(archer_left, left_position)
        self.screen.blit(archer_right, right_position)

        # Calculer la position centrée pour la case à cocher et le texte
        checkbox_text = "Ajouter un obstacle"
        checkbox_text_surf = self.font.render(checkbox_text, True, (255, 255, 255))
        checkbox_text_rect = checkbox_text_surf.get_rect()

        # Positionner la case à cocher et le texte
        checkbox_text_rect.centerx = self.width // 2
        checkbox_text_rect.top = 100  # Espacement vertical au-dessus du texte

        # Ajuster la position de la case à cocher pour aligner avec le texte
        self.checkbox_rect.midright = (checkbox_text_rect.left - 10, checkbox_text_rect.centery)

        # Changer la couleur de la case à cocher si l'option d'obstacle est activée
        if self.obstacle_option:
            self.checkbox_color = (0, 255, 0)  # Couleur verte
        else:
            self.checkbox_color = (255, 255, 255)  # Couleur blanche

        # Dessiner la case à cocher avec la couleur mise à jour
        pygame.draw.rect(self.screen, self.checkbox_color, self.checkbox_rect)

        if self.obstacle_option:
            # Dessiner le tick (signe validé) en vert
            self.draw_tick(self.checkbox_rect, self.tick_color)
        
        # Dessiner le texte
        self.screen.blit(checkbox_text_surf, checkbox_text_rect.topleft)

        # Liste des autres informations
        lines = [
            f"Background: {self.selected_background} (Press B to change)",
            f"Style: {self.selected_style} (Press S to change)",
            f"Mode: {self.play_mode} (Press M to change)",
            f"Arrow Color: {self.selected_arrow_color_name} (Press C to change)",
            "",  # Ligne vide pour l'espace
            "Press ENTER to start"
        ]

        line_height = 40
        padding = 10
        box_width = max(self.font.size(line)[0] for line in lines if line) + 2 * padding
        start_y = checkbox_text_rect.bottom + 20  # Déplacer vers le bas pour laisser de l'espace

        current_y = start_y
        for line in lines:
            if line:  # Ne pas dessiner les boîtes pour les lignes vides
                text_surf = self.font.render(line, True, (245, 245, 220))  # Beige
                self.screen.blit(text_surf, (self.width // 2 - text_surf.get_width() // 2, current_y))
            current_y += line_height
        
        self.screen.blit(self.back_button_img, self.back_button_rect.topleft)

        pygame.display.flip()


    def draw_tick(self, rect, color):
        """Dessiner un tick dans la case à cocher"""
        # Calculer les points pour le tick
        x, y, w, h = rect
        margin = 4
        pygame.draw.line(self.screen, color, (x + margin, y + h // 2), (x + w // 2, y + h - margin), 3)
        pygame.draw.line(self.screen, color, (x + w // 2, y + h - margin), (x + w - margin, y + margin), 3)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return {"action": "main_menu"}
                elif event.key == pygame.K_RETURN:
                    return {
                        "action": "start_game", 
                        "background": self.selected_background, 
                        "style": self.selected_style, 
                        "play_mode": self.play_mode,
                        "arrow_color": self.selected_arrow_color,
                        "add_obstacle": self.obstacle_option
                    }
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
                elif event.key == pygame.K_c:
                    # Changer la couleur de la tige de la flèche
                    current_index = self.arrow_color_names.index(self.selected_arrow_color_name)
                    self.selected_arrow_color_name = self.arrow_color_names[(current_index + 1) % len(self.arrow_color_names)]
                    self.selected_arrow_color = self.arrow_colors[self.selected_arrow_color_name]
                elif event.key == pygame.K_o:
                    # Basculer l'option de l'obstacle
                    self.obstacle_option = not self.obstacle_option
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.checkbox_rect.collidepoint(event.pos):
                        # Inverser l'état de la case à cocher lorsqu'on clique dessus
                        self.obstacle_option = not self.obstacle_option
                    elif self.back_button_rect.collidepoint(event.pos):
                        return {"action": "main_menu"}  # Retour au menu principal
        return None

    def run(self):
        while True:
            result = self.handle_events()
            if result:
                if result["action"] == "start_game":
                    game = GameScene(self.screen, {
                        "background": result["background"],
                        "style": result["style"],
                        "play_mode": result["play_mode"],
                        "arrow_color": result["arrow_color"],
                        "add_obstacle": result["add_obstacle"]
                    })
                    game.run()
                elif result["action"] == "main_menu":
                    return
            self.draw()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man')

    game = CustomizationScene(screen)
    settings = game.run()
