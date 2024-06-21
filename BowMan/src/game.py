import pygame
import sys
import os
from pauseMenu import PauseMenu
from optionsMenu import OptionsMenu
from endGameMenu import EndGameMenu

class Ball:
    def __init__(self, screen, start_x, start_y, x_velocity, y_velocity):
        self.screen = screen
        self.x = start_x
        self.y = start_y
        self.radius = 10
        self.color = (255, 0, 0)
        self.gravity = 0.5
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.damage = 10

    def update(self):
        self.x += self.x_velocity
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        if self.y + self.radius > self.screen.get_height():
            self.y = self.screen.get_height() - self.radius
            self.y_velocity = 0
            self.x_velocity = 0

    def draw(self, camera_x):
        pygame.draw.circle(self.screen, self.color, (int(self.x - camera_x), int(self.y)), self.radius)

class Archer:
    def __init__(self, image, x, y, screen):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen = screen
        self.health = 30

    def draw(self, camera_x):
        self.screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        self.draw_health(camera_x)

    def draw_health(self, camera_x):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (self.rect.x - camera_x, self.rect.y - 30))

class Obstacle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.color = (100, 100, 100)
        self.rect1 = pygame.Rect(x, y, width, height // 2)
        self.rect2 = pygame.Rect(x, y + height // 2, width, height // 2)

    def draw(self, camera_x):
        pygame.draw.rect(self.screen, self.color, self.rect1.move(-camera_x, 0))
        pygame.draw.rect(self.screen, self.color, self.rect2.move(-camera_x, 0))

class Game:
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
        self.pause_menu = PauseMenu(screen)

        self.balls = []
        self.obstacle = Obstacle(self.screen, self.scene_width // 2 - 100, self.scene_height - 50, 200, 400)  # Initialisation de l'obstacle

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_a and not self.paused:
                    new_ball = Ball(self.screen, self.archer_left.rect.right, self.archer_left.rect.centery, 50, -10)
                    self.balls.append(new_ball)
                elif event.key == pygame.K_q and not self.paused:
                    new_ball = Ball(self.screen, self.archer_right.rect.left, self.archer_right.rect.centery, -50, -10)
                    self.balls.append(new_ball)
                elif event.key == pygame.K_o:  # Touche 'o' pour placer un obstacle
                    self.obstacle = Obstacle(self.screen, self.scene_width // 2 - 100, self.scene_height - 150, 200, 800)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.paused:
                    self.move_camera_right = not self.move_camera_right
                elif self.paused:
                    action = self.pause_menu.handle_events()
                    if action == "continue":
                        self.paused = False
                    elif action == "options":
                        options_menu = OptionsMenu(self.screen)
                        options_menu.run()
                    elif action == "main_menu":
                        from mainMenu import MainMenu
                        main_menu = MainMenu(self.screen)
                        main_menu.run()
                        pygame.quit()
                        sys.exit()
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

    def check_collisions(self):
        for ball in self.balls:
            if ball.x - ball.radius < self.archer_left.rect.right and ball.x + ball.radius > self.archer_left.rect.left and ball.y - ball.radius < self.archer_left.rect.bottom and ball.y + ball.radius > self.archer_left.rect.top:
                self.archer_left.health -= ball.damage
                self.balls.remove(ball)
                if self.archer_left.health <= 0:
                    end_game_menu = EndGameMenu(self.screen, "Archer Droit")
                    end_game_menu.run()

            elif ball.x - ball.radius < self.archer_right.rect.right and ball.x + ball.radius > self.archer_right.rect.left and ball.y - ball.radius < self.archer_right.rect.bottom and ball.y + ball.radius > self.archer_right.rect.top:
                self.archer_right.health -= ball.damage
                self.balls.remove(ball)
                if self.archer_right.health <= 0:
                    end_game_menu = EndGameMenu(self.screen, "Archer Gauche")
                    end_game_menu.run()

    def update(self):
        if self.move_camera_right and self.camera_x < (self.scene_width - self.width):
            self.camera_x += self.camera_speed
            if self.camera_x > (self.scene_width - self.width):
                self.camera_x = self.scene_width - self.width
        elif not self.move_camera_right and self.camera_x > 0:
            self.camera_x -= self.camera_speed
            if self.camera_x < 0:
                self.camera_x = 0

        for ball in self.balls:
            ball.update()

        self.check_collisions()

    def draw(self):
        self.screen.blit(self.background_img, (-self.camera_x, 0))

        self.archer_left.draw(self.camera_x)
        self.archer_right.draw(self.camera_x)

        self.obstacle.draw(self.camera_x)  # Dessiner l'obstacle

        for ball in self.balls:
            ball.draw(self.camera_x)

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
                    options_menu = OptionsMenu(self.screen)
                    options_menu.run()
                elif action == "main_menu":
                    from mainMenu import MainMenu
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

    game = Game(screen)
    game.run()
