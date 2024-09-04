import pygame
import random
import math
#from arrow import Arrow

class IA:
    def __init__(self, archer, screen, obstacle, arrows, turn):
        self.archer = archer
        self.screen = screen
        self.obstacle = obstacle
        self.arrows = arrows
        self.turn = turn
        self.shoot_power = 20
        self.shoot_angle = 45
        self.last_shot_distance = None
        self.target_x = random.randint(50, screen.get_width() - 50)
        self.target_y = random.randint(50, screen.get_height() - 50)
        self.initial_shot = True

    def decide_action(self):
        if self.initial_shot:
            self.shoot_random()
            self.initial_shot = False
        else:
            self.adjust_shooting_parameters()
            self.shoot()

    def shoot_random(self):
        # Tir aléatoire sans ajustement
        self.shoot_power = random.randint(10, 50)
        self.shoot_angle = random.uniform(0, 90)
        self.shoot()

    def adjust_shooting_parameters(self):
        if self.last_shot_distance is not None:
            # Ajuster la puissance et l'angle en fonction de la distance du dernier tir
            if self.last_shot_distance < 100:
                self.shoot_power = min(self.shoot_power + 5, 100)
            elif self.last_shot_distance > 200:
                self.shoot_power = max(self.shoot_power - 5, 10)

            if self.last_shot_distance < 100:
                self.shoot_angle = min(self.shoot_angle + 5, 90)
            elif self.last_shot_distance > 200:
                self.shoot_angle = max(self.shoot_angle - 5, 0)
                
    def shoot(self):
        # Tirer une flèche avec les paramètres calculés
        angle_radians = math.radians(self.shoot_angle)
        x_velocity = self.shoot_power * math.cos(angle_radians)
        y_velocity = -self.shoot_power * math.sin(angle_radians)

        #if self.turn == 'left':
            #new_arrow = Arrow(self.screen, self.archer.rect.right, self.archer.rect.centery, x_velocity, y_velocity)
        #else:
            #new_arrow = Arrow(self.screen, self.archer.rect.left, self.archer.rect.centery, -x_velocity, y_velocity)
        
        #self.arrows.append(new_arrow)
        
        # Mettre à jour la distance du dernier tir
        #self.last_shot_distance = math.hypot(new_arrow.x - self.target_x, new_arrow.y - self.target_y)

    def update(self):
        # Décider de l'action à chaque mise à jour
        self.decide_action()
