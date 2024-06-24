import pygame

class Obstacle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.color = (100, 100, 100)
        self.rect1 = pygame.Rect(x, y, width, height // 2)
        self.rect2 = pygame.Rect(x, y + height // 2, width, height // 2)

    def draw(self, camera_x):
        pygame.draw.rect(self.screen, self.color, self.rect1.move(-camera_x, 0))
        pygame.draw.rect(self.screen, self.color, self.rect2.move(-camera_x, 0))
