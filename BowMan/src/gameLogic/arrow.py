import pygame
import math

class Arrow:
    def __init__(self, screen, start_x, start_y, x_velocity, y_velocity):
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
        self.color = (139, 69, 19)  # Couleur marron pour la flèche
        self.tip_color = (0, 255, 0)  # Couleur verte pour la pointe de la flèche

    def update(self):
        self.x += self.x_velocity
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        if self.y >= self.ground_level:
            self.y = self.ground_level
            self.y_velocity = 0
            self.x_velocity = 0

        # Calculer l'angle de la flèche par rapport à l'horizontale
        self.angle = math.degrees(math.atan2(self.y_velocity, self.x_velocity))

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
        pygame.draw.polygon(self.screen, self.tip_color, [(int(end_x - camera_x), int(end_y)),
                                                          (int(tip1_x - camera_x), int(tip1_y)),
                                                          (int(tip2_x - camera_x), int(tip2_y))])
