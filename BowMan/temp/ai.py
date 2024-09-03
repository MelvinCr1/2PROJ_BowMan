import pygame
import random
import math
from gameLogic.arrow import Arrow

class AI:
    def __init__(self, image, x, y, screen):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen = screen
        self.health = 30
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_interval = 2000  # Intervalle entre les tirs de l'IA en millisecondes
        self.ready_to_shoot = True  # Indicateur pour savoir si l'IA est prête à tirer

    def draw(self, camera_x):
        self.screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        self.draw_health(camera_x)

    def draw_health(self, camera_x):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"AI HP: {self.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (self.rect.x - camera_x, self.rect.y - 30))

    def update(self, player_has_shot, arrows):
        current_time = pygame.time.get_ticks()

        # Déclenche le tir automatique si l'IA est prête et que l'intervalle est passé
        if player_has_shot and (current_time - self.last_shot_time > self.shoot_interval):
            self.shoot(arrows)
            self.last_shot_time = current_time
            self.ready_to_shoot = False

        # Réinitialiser la disponibilité de tir de l'IA après un certain temps
        if not self.ready_to_shoot and (current_time - self.last_shot_time > self.shoot_interval):
            self.ready_to_shoot = True

    def shoot(self, arrows):
        angle_radians = random.uniform(0, math.pi / 2)  # Angle aléatoire
        x_velocity = 20 * math.cos(angle_radians)
        y_velocity = -20 * math.sin(angle_radians)
        new_arrow = Arrow(self.screen, self.rect.left, self.rect.centery, x_velocity, y_velocity)
        arrows.append(new_arrow)  # Ajoutez la flèche à la liste
