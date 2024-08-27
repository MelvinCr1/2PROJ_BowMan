import pygame
import math

class Arrow:
    def __init__(self, screen, start_x, start_y, x_velocity, y_velocity, color=(139, 69, 19), tip_color=(0, 255, 0)):
        self.screen = screen
        self.x = start_x
        self.y = start_y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.gravity = 0.5
        self.damage = 10
        self.ground_level = self.screen.get_height() - 50  # Niveau du sol
        
        # Paramètres de la flèche
        self.length = 30
        self.color = color  # Couleur de la flèche
        self.tip_color = tip_color  # Couleur de la pointe de la flèche

        # Créer un rect pour la flèche (pour les collisions)
        self.rect = pygame.Rect(self.x, self.y, self.length, 3)  # La hauteur de 3 pixels est choisie pour représenter l'épaisseur de la flèche

    def update(self):
        self.x += self.x_velocity
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        # Mise à jour du rectangle pour suivre la position de la flèche
        self.rect.x = self.x
        self.rect.y = self.y

        if self.y >= self.ground_level:
            self.y = self.ground_level
            self.y_velocity = 0
            self.x_velocity = 0

        # Calculer l'angle de la flèche par rapport à l'horizontale
        self.angle = math.degrees(math.atan2(self.y_velocity, self.x_velocity))

        # Ajuster la position du rect en fonction de l'angle et de la longueur de la flèche
        self.rect = pygame.Rect(self.x, self.y, self.length, 3)
        self.rect.topleft = (self.x - self.length / 2, self.y - 1.5)  # Ajustement pour centrer le rect

    def draw(self, camera_x):
        # Calculer les coordonnées de l'extrémité de la flèche
        end_x = self.x - self.length * math.cos(math.radians(self.angle))
        end_y = self.y - self.length * math.sin(math.radians(self.angle))

        # Dessiner la ligne principale de la flèche
        pygame.draw.line(self.screen, self.color, (int(self.x - camera_x), int(self.y)), (int(end_x - camera_x), int(end_y)), 3)

        # Calculer les coordonnées pour dessiner la pointe de la flèche
        arrow_tip_length = 10  # Longueur de la pointe de la flèche
        arrow_tip_angle = math.radians(30)  # Angle de la pointe de la flèche par rapport à l'axe de la flèche

        tip1_x = end_x - arrow_tip_length * math.cos(math.radians(self.angle) + arrow_tip_angle)
        tip1_y = end_y - arrow_tip_length * math.sin(math.radians(self.angle) + arrow_tip_angle)

        tip2_x = end_x - arrow_tip_length * math.cos(math.radians(self.angle) - arrow_tip_angle)
        tip2_y = end_y - arrow_tip_length * math.sin(math.radians(self.angle) - arrow_tip_angle)

        # Dessiner la pointe de la flèche
        pygame.draw.polygon(self.screen, self.tip_color, [
            (int(end_x - camera_x), int(end_y)),
            (int(tip1_x - camera_x), int(tip1_y)),
            (int(tip2_x - camera_x), int(tip2_y))
        ])

        # Mettre à jour la position du rect pour correspondre à la position actuelle de la flèche
        self.rect.topleft = (self.x - camera_x, self.y)
