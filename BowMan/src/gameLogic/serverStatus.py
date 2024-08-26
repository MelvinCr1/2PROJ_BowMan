# serverStatus.py
import pygame
import socket

class ServerStatus:
    def __init__(self, screen, font_size=24):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.is_running = False
        self.server_status = "Server Status: Unknown"
        self.connected_ips = []

    def update_status(self, status, ips):
        self.server_status = status
        self.connected_ips = ips

    def draw(self):
        # Définir la couleur du texte
        text_color = (255, 255, 255)
        
        # Obtenir la largeur et la hauteur de l'écran
        screen_width, screen_height = self.screen.get_size()
        
        # Calculer les positions pour le texte en haut à droite
        y = 50
        status_text = self.font.render(self.server_status, True, text_color)
        status_rect = status_text.get_rect(topright=(screen_width - 10, y))
        self.screen.blit(status_text, status_rect.topleft)
        y += status_rect.height + 10  # Espace entre les lignes

        for ip in self.connected_ips:
            ip_text = self.font.render(f"Connected IP: {ip}", True, text_color)
            ip_rect = ip_text.get_rect(topright=(screen_width - 10, y))
            self.screen.blit(ip_text, ip_rect.topleft)
            y += ip_rect.height + 10  # Espace entre les lignes
