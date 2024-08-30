from pygame.locals import *
import pygame
import random
import sys
import os
import math
from pauseScene import PauseScene
from optionsScene import OptionsScene
from endGameScene import EndGameScene
from gameLogic.arrow import Arrow
from gameLogic.archer import Archer
from gameLogic.obstacle import Obstacle
from gameLogic.ai import AI  # Importer la classe IA
from gameLogic.serverStatus import ServerStatus

class GameScene:
    def __init__(self, screen, settings):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '../assets/')

        self.scene_width, self.scene_height = 2400, 800
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.settings = settings
        self.obstacle = None

        self.background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds', settings["background"])).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.scene_width, self.scene_height))

        # Ajuster la taille des archers
        archer_scale_factor = 0.5  # Réduire la taille des archers à 50%
        archer_img_left = pygame.image.load(os.path.join(assets_path, 'characters', settings["style"])).convert_alpha()
        archer_original_width, archer_original_height = archer_img_left.get_size()
        archer_img_left = pygame.transform.scale(archer_img_left, (int(archer_original_width * archer_scale_factor), int(archer_original_height * archer_scale_factor)))
        archer_img_right = pygame.transform.flip(archer_img_left, True, False)
        self.archer_left = Archer(archer_img_left, 50, self.height // 2 - archer_img_left.get_height() // 2, self.screen)
        self.archer_right = Archer(archer_img_right, self.scene_width - 250, self.height // 2 - archer_img_right.get_height() // 2, self.screen)

        # Hauteur pour tous les archers
        custom_y = 450

        # Distance minimale pour s'assurer que les archers ne se voient pas
        min_distance = 600

        # Position des archers dans leurs moitiés respectives avec une distance minimale
        max_left_x = (self.scene_width // 2) - min_distance - archer_img_left.get_width()
        min_right_x = (self.scene_width // 2) + min_distance

        archer_left_x = random.randint(50, max_left_x)  # Gauche
        archer_right_x = random.randint(min_right_x, self.scene_width - 200)  # Droite

        self.archer_left = Archer(archer_img_left, archer_left_x, custom_y, self.screen)
        self.archer_right = Archer(archer_img_right, archer_right_x, custom_y, self.screen)


        # Initialiser l'IA
        self.ai = AI(archer_img_right, self.scene_width - 250, self.height // 2 - archer_img_right.get_height() // 2, self.screen)

        self.camera_x = 0
        self.camera_speed = 20
        self.move_camera_right = False

        self.paused = False
        self.pause_menu = PauseScene(screen)

        self.arrows = []
        self.obstacle = Obstacle(self.screen, x=self.scene_width // 2 - 200, y=self.scene_height - 600, width=400, height=600)


        self.turn = 'left'

        self.shoot_power = 20
        self.shoot_angle = 45

        self.start_time = pygame.time.get_ticks()

        if settings.get("play_mode") == "multiplayer":
            self.server_status = ServerStatus(screen)
            self.server_status.update_status("Server Unknown", ["Unknown", "Unknown"])

        self.arrow_color = settings.get("arrow_color", (0, 255, 0))  # Vert par défaut
        self.add_obstacle = settings.get("add_obstacle", False)  # Par défaut, pas d'obstacle

        # Print le mode de jeu sélectionné
        print(f"Mode de jeu sélectionné : {settings.get('play_mode', 'non défini')}")

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
                        "add_obstacle": self.obstacle_option  # Passer l'option d'ajout d'obstacle
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
                    # Basculer l'option d'obstacle
                    self.obstacle_option = not self.obstacle_option
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.checkbox_rect.collidepoint(event.pos):
                        # Inverser l'état de la case à cocher lorsqu'on clique dessus
                        self.obstacle_option = not self.obstacle_option
                    elif self.back_button_rect.collidepoint(event.pos):
                        return {"action": "main_menu"}  # Retour au menu principal
        return None


    def check_collisions(self):
        for arrow in self.arrows:
            # Collision avec l'archer gauche
            if (self.archer_left.rect.left < arrow.x < self.archer_left.rect.right and self.archer_left.rect.top < arrow.y < self.archer_left.rect.bottom):
                self.archer_left.health -= arrow.damage
                self.arrows.remove(arrow)
                if self.archer_left.health <= 0:
                    end_game_menu = EndGameScene(self.screen, "Archer Gauche")
                    end_game_menu.run()

            # Collision avec l'archer droit
            elif (self.archer_right.rect.left < arrow.x < self.archer_right.rect.right and self.archer_right.rect.top < arrow.y < self.archer_right.rect.bottom):
                self.archer_right.health -= arrow.damage
                self.arrows.remove(arrow)
                if self.archer_right.health <= 0:
                    end_game_menu = EndGameScene(self.screen, "Archer Droit")
                    end_game_menu.run()

            # Collision avec l'obstacle
            if self.obstacle.contains_point(arrow.x, arrow.y):
                self.arrows.remove(arrow)


    def update(self):
        if self.arrows:
            arrow = self.arrows[-1]
            target_camera_x = arrow.x - self.width // 2

            if target_camera_x < 0:
                target_camera_x = 0
            elif target_camera_x > self.scene_width - self.width:
                target_camera_x = self.scene_width - self.width

            self.camera_x += (target_camera_x - self.camera_x) * 0.1

        for arrow in self.arrows:
            arrow.update()

        self.check_collisions()

        # Mettre à jour l'IA
        if self.settings["play_mode"] == "IA":
            self.ai.update(self.arrows)

    def draw_server_status_indicator(self):
        # Définir la couleur du cercle en fonction du statut du serveur
        if self.settings.get("play_mode") == "multiplayer":
            if self.server_status.is_running:
                color = (0, 255, 0)  # Vert pour serveur actif
            else:
                color = (255, 0, 0)  # Rouge pour serveur inactif
            pygame.draw.circle(self.screen, color, (self.width - 30, 30), 10)

    def draw(self):
        self.screen.blit(self.background_img, (-self.camera_x, 0))

        self.archer_left.draw(self.camera_x)
        self.archer_right.draw(self.camera_x)
        
        # Dessiner l'IA et sa vie seulement si le mode de jeu est IA
        if self.settings.get("play_mode") == "IA":
            self.ai.draw(self.camera_x)
        
        # Dessiner l'obstacle seulement s'il est présent
        if self.add_obstacle:
            self.draw_obstacle()

        for arrow in self.arrows:
            arrow.draw(self.camera_x)

        # Dessiner le statut du serveur
        if self.settings.get("play_mode") == "multiplayer":
            self.draw_server_status_indicator()
            self.server_status.draw()  # Dessiner le statut du serveur après l'indicateur

        # Power / angle texts
        font = pygame.font.Font(None, 36)
        power_text = font.render(f"Power: {self.shoot_power} (< >)", True, (255, 255, 255))
        angle_text = font.render(f"Angle: {self.shoot_angle} (^ v️)", True, (255, 255, 255))
        self.screen.blit(power_text, (10, 10))
        self.screen.blit(angle_text, (10, 50))

        # Timer
        elapsed_time_ms = pygame.time.get_ticks() - self.start_time
        seconds = (elapsed_time_ms // 1000) % 60
        minutes = (elapsed_time_ms // 60000) % 60
        hours = (elapsed_time_ms // 3600000) % 24
        timer_text = font.render(f"{hours:02}:{minutes:02}:{seconds:02}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(self.width // 2, 30))  # Center horizontally, 30 pixels from the top
        self.screen.blit(timer_text, timer_rect.topleft)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.handle_events()
            
            if not self.paused:
                self.update()
                self.draw()
            else:
                self.pause_menu.draw()  # Afficher l'interface de pause
                action = self.pause_menu.handle_events()
                if action == "continue":
                    self.paused = False
                elif action == "options":
                    options_menu = OptionsScene(self.screen)
                    options_menu.run()
                elif action == "main_menu":
                    from mainScene import MainMenu
                    main_menu = MainMenu(self.screen)
                    main_menu.run()
                    running = False
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man')

    settings = {
        "background": "background1.jpg",
        "style": "archer.png",
        "play_mode": "local",
        "arrow_color": (0, 255, 0)  # Couleur de la pointe par défaut
    }
    game = GameScene(screen, settings)
    game.run()
