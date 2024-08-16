import pygame

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
        
        # Calculer la position du texte de la santé pour qu'il soit centré au-dessus de l'archer
        health_text_rect = health_text.get_rect(midbottom=(self.rect.centerx - camera_x, self.rect.y - 10))
        
        self.screen.blit(health_text, health_text_rect.topleft)
