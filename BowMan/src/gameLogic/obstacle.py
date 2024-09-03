import pygame
import random

class Obstacle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.color = (100, 100, 100)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.width = max(width, 400)
        self.height = max(height, 600)

        # Position de l'obstacle pour qu'il touche le sol
        self.y = self.screen.get_height() - self.height

        # Points pour dessiner un rocher irrégulier
        self.points = self.generate_random_points()

        # Collision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def generate_random_points(self):
        num_points = 7  # Nombre de points pour dessiner le rocher
        points = []

        # Génération des points / marges pour assurer une taille minimale
        for _ in range(num_points):
            px = self.x + random.uniform(0, self.width)
            py = self.y + random.uniform(0, self.height)
            points.append((px, py))

        # algorithme de convex hull pour générer une forme convexe
        return self.convex_hull(points)

    def convex_hull(self, points):
        # Algorithme de Graham Scan pour trouver le convex hull
        points = sorted(points)  # Trier les points
        if len(points) <= 1:
            return points
        
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        
        return lower[:-1] + upper[:-1]

    def draw(self, camera_x):
        # Ajuster les points en fonction de la position de la caméra
        adjusted_points = [(px - camera_x, py) for px, py in self.points]
        
        # Polygone qui représente le rocher
        pygame.draw.polygon(self.screen, self.color, adjusted_points)

    def contains_point(self, x, y):
        # Algorithme de ray-casting pour vérifier si un point est à l'intérieur du polygone
        num_points = len(self.points)
        inside = False
        p1x, p1y = self.points[0]
        for i in range(num_points + 1):
            p2x, p2y = self.points[i % num_points]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
