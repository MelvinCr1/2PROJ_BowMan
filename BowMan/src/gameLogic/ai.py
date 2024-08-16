import pygame
import random
import math
from .arrow import Arrow

class AI:
    def __init__(self, image, x, y, screen):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen = screen
        self.health = 30
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_interval = 2000  # Intervalle entre les tirs de l'IA en millisecondes

    def draw(self, camera_x):
        self.screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        self.draw_health(camera_x)

    def draw_health(self, camera_x):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (self.rect.x - camera_x, self.rect.y - 30))

    def update(self, arrows):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.shoot(arrows)
            self.last_shot_time = current_time

    def shoot(self, arrows):
        angle_radians = random.uniform(0, math.pi / 2)  # Angle aléatoire
        x_velocity = 20 * math.cos(angle_radians)
        y_velocity = -20 * math.sin(angle_radians)
        new_arrow = Arrow(self.screen, self.rect.left, self.rect.centery, x_velocity, y_velocity)
        arrows.append(new_arrow)
