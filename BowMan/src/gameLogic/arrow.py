import pygame

class Arrow:
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
