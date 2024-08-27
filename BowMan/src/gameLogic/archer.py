import pygame

class Archer:
    def __init__(self, image, x, y, screen):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen = screen
        self.health = 30

    def draw(self, camera_x):
        # Dessiner l'archer
        self.screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        # Dessiner la barre de vie
        self.draw_health(camera_x)

    def draw_health(self, camera_x):
        # Position de la barre de vie
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.rect.x - camera_x + (self.rect.width - health_bar_width) // 2
        health_bar_y = self.rect.y - 30

        # Dessiner le fond de la barre de vie
        pygame.draw.rect(self.screen, (0, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # Calculer le pourcentage de vie restant
        health_percentage = max(self.health / 30.0, 0)  # Assurez-vous que la division ne dépasse pas 1
        
        # Dessiner la barre de vie en couleur, s'assurer que la largeur ne dépasse pas la largeur de la barre de vie
        pygame.draw.rect(self.screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width * health_percentage, health_bar_height))

        # Dessiner le texte de la vie
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"HP: {self.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (health_bar_x, health_bar_y - 20))
