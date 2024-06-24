from pygame.locals import *
import pygame
import sys
import os
import math
from pauseScene import PauseScene
from optionsScene import OptionsScene
from endGameScene import EndGameScene
from gameLogic.arrow import Arrow
from gameLogic.archer import Archer
from gameLogic.obstacle import Obstacle

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '../assets/')

        self.scene_width, self.scene_height = 2400, 800
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds/background1.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.scene_width, self.scene_height))

        archer_img_left = pygame.image.load(os.path.join(assets_path, 'characters/archer.png')).convert_alpha()
        archer_img_left = pygame.transform.scale(archer_img_left, (200, 400))

        archer_img_right = pygame.transform.flip(archer_img_left, True, False)

        self.archer_left = Archer(archer_img_left, 50, self.height // 2 - archer_img_left.get_height() // 2, self.screen)
        self.archer_right = Archer(archer_img_right, self.scene_width - 250, self.height // 2 - archer_img_right.get_height() // 2, self.screen)

        self.camera_x = 0
        self.camera_speed = 20
        self.move_camera_right = False

        self.paused = False
        self.pause_menu = PauseScene(screen)

        self.arrows = []  # Utiliser des flèches à la place de balls
        self.obstacle = Obstacle(self.screen, self.scene_width // 2 - 100, self.scene_height - 50, 200, 400)

        self.turn = 'left'

        self.shoot_power = 20
        self.shoot_angle = 45

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_a and not self.paused:
                    angle_radians = math.radians(self.shoot_angle)
                    x_velocity = self.shoot_power * math.cos(angle_radians)
                    y_velocity = -self.shoot_power * math.sin(angle_radians)

                    if self.turn == 'left':
                        new_arrow = Arrow(self.screen, self.archer_left.rect.right, self.archer_left.rect.centery, x_velocity, y_velocity)
                        self.arrows.append(new_arrow)
                        self.turn = 'right'
                    elif self.turn == 'right':
                        new_arrow = Arrow(self.screen, self.archer_right.rect.left, self.archer_right.rect.centery, -x_velocity, y_velocity)
                        self.arrows.append(new_arrow)
                        self.turn = 'left'
                elif event.key == pygame.K_o:
                    self.obstacle = Obstacle(self.screen, self.scene_width // 2 - 100, self.scene_height - 150, 200, 800)
                elif event.key == pygame.K_UP:
                    self.shoot_angle += 1
                    if self.shoot_angle > 90:
                        self.shoot_angle = 90
                elif event.key == pygame.K_DOWN:
                    self.shoot_angle -= 1
                    if self.shoot_angle < 0:
                        self.shoot_angle = 0
                elif event.key == pygame.K_RIGHT:
                    self.shoot_power += 1
                    if self.shoot_power > 100:
                        self.shoot_power = 100
                elif event.key == pygame.K_LEFT:
                    self.shoot_power -= 1
                    if self.shoot_power < 1:
                        self.shoot_power = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.paused:
                    self.move_camera_right = not self.move_camera_right
                elif self.paused:
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
                        pygame.quit()
                        sys.exit()
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

    def check_collisions(self):
        for arrow in self.arrows:
            if arrow.x < self.archer_left.rect.right and arrow.x > self.archer_left.rect.left and arrow.y < self.archer_left.rect.bottom and arrow.y > self.archer_left.rect.top:
                self.archer_left.health -= arrow.damage
                self.arrows.remove(arrow)
                if self.archer_left.health <= 0:
                    end_game_menu = EndGameScene(self.screen, "Archer Gauche")
                    end_game_menu.run()

            elif arrow.x < self.archer_right.rect.right and arrow.x > self.archer_right.rect.left and arrow.y < self.archer_right.rect.bottom and arrow.y > self.archer_right.rect.top:
                self.archer_right.health -= arrow.damage
                self.arrows.remove(arrow)
                if self.archer_right.health <= 0:
                    end_game_menu = EndGameScene(self.screen, "Archer Droit")
                    end_game_menu.run()

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

    def draw(self):
        self.screen.blit(self.background_img, (-self.camera_x, 0))

        self.archer_left.draw(self.camera_x)
        self.archer_right.draw(self.camera_x)

        self.obstacle.draw(self.camera_x)

        for arrow in self.arrows:
            arrow.draw(self.camera_x)

        font = pygame.font.Font(None, 36)
        power_text = font.render(f"Power: {self.shoot_power} (< >)", True, (255, 255, 255))
        angle_text = font.render(f"Angle: {self.shoot_angle} (^ v️)", True, (255, 255, 255))
        self.screen.blit(power_text, (10, 10))
        self.screen.blit(angle_text, (10, 50))

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            self.handle_events()
            if not self.paused:
                self.update()
                self.draw()
            else:
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

    game = GameScene(screen)
    game.run()
