import pygame
import sys
import os
from pauseMenu import PauseMenu  # Importez la classe PauseMenu
from optionsMenu import OptionsMenu  # Importez la classe OptionsMenu

class Ball:
    def __init__(self, screen, start_x, start_y, x_velocity, y_velocity):
        self.screen = screen
        self.x = start_x
        self.y = start_y
        self.radius = 10
        self.color = (255, 0, 0)
        self.gravity = 0.5  # Gravité
        self.x_velocity = x_velocity  # Vitesse horizontale
        self.y_velocity = y_velocity  # Vitesse verticale initiale

    def update(self):
        self.x += self.x_velocity
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        # Limiter la balle au bas de l'écran
        if self.y + self.radius > self.screen.get_height():
            self.y = self.screen.get_height() - self.radius
            self.y_velocity = 0  # Arrêter la chute
            self.x_velocity = 0  # Arrêter le mouvement horizontal

    def draw(self, camera_x):
        pygame.draw.circle(self.screen, self.color, (int(self.x - camera_x), int(self.y)), self.radius)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Chemin absolu vers le dossier assets depuis le répertoire principal
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '../assets/')  # Ajustez selon votre structure

        # Définir les nouvelles dimensions de la fenêtre de jeu
        self.scene_width, self.scene_height = 2400, 800  # Taille totale de la scène
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Charger l'image de fond
        self.background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds/background1.jpg')).convert()
        self.background_img = pygame.transform.scale(self.background_img, (self.scene_width, self.scene_height))

        # Charger l'image de l'archer
        self.archer_img_left = pygame.image.load(os.path.join(assets_path, 'characters/archer.png')).convert_alpha()
        self.archer_img_left = pygame.transform.scale(self.archer_img_left, (200, 400))  # Ajuster la taille de l'archer

        # Inverser l'image de l'archer pour la droite
        self.archer_img_right = pygame.transform.flip(self.archer_img_left, True, False)

        # Rectangles pour positionner les archers
        self.archer_left_rect = self.archer_img_left.get_rect(
            topleft=(50, self.height // 2 - self.archer_img_left.get_height() // 2))
        self.archer_right_rect = self.archer_img_right.get_rect(
            topright=(self.scene_width - 50, self.height // 2 - self.archer_img_right.get_height() // 2))

        # Initialisation de la caméra
        self.camera_x = 0  # Position initiale de la caméra
        self.camera_speed = 20  # Vitesse de déplacement de la caméra
        self.move_camera_right = False  # Indique si la caméra doit se déplacer vers la droite

        # Etat du jeu
        self.paused = False
        self.pause_menu = PauseMenu(screen)  # Créer une instance du menu pause

        # Liste pour stocker les balles
        self.balls = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_a and not self.paused:  # Touche 'a' pour lancer une balle depuis l'archer gauche
                    new_ball = Ball(self.screen, self.archer_left_rect.right, self.archer_left_rect.centery, 15, -20)
                    self.balls.append(new_ball)
                elif event.key == pygame.K_q and not self.paused:  # Touche 'q' pour lancer une balle depuis l'archer droit
                    new_ball = Ball(self.screen, self.archer_right_rect.left, self.archer_right_rect.centery, -15, -10)
                    self.balls.append(new_ball)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.paused:  # Bouton gauche de la souris
                    self.move_camera_right = not self.move_camera_right
                elif self.paused:  # Si le jeu est en pause, gérer les événements du menu pause
                    action = self.pause_menu.handle_events()
                    if action == "continue":
                        self.paused = False
                    elif action == "options":
                        options_menu = OptionsMenu(self.screen)  # Créer une instance du menu des options
                        options_menu.run()
                    elif action == "main_menu":
                        from mainMenu import MainMenu  # Importer ici pour éviter l'import circulaire
                        main_menu = MainMenu(self.screen)  # Créer une instance du menu principal
                        main_menu.run()
                        pygame.quit()
                        sys.exit()
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

    def update(self):
        # Déplacer la caméra
        if self.move_camera_right and self.camera_x < (self.scene_width - self.width):
            self.camera_x += self.camera_speed
            if self.camera_x > (self.scene_width - self.width):
                self.camera_x = self.scene_width - self.width
        elif not self.move_camera_right and self.camera_x > 0:
            self.camera_x -= self.camera_speed
            if self.camera_x < 0:
                self.camera_x = 0

        # Mettre à jour les balles
        for ball in self.balls:
            ball.update()

    def draw(self):
        # Afficher la partie visible de la scène
        self.screen.blit(self.background_img, (-self.camera_x, 0))

        # Afficher les deux archers
        self.screen.blit(self.archer_img_left, (self.archer_left_rect.x - self.camera_x, self.archer_left_rect.y))
        self.screen.blit(self.archer_img_right, (self.archer_right_rect.x - self.camera_x, self.archer_right_rect.y))

        # Dessiner les balles
        for ball in self.balls:
            ball.draw(self.camera_x)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            self.handle_events()
            if not self.paused:
                self.update()
                self.draw()
            else:
                action = self.pause_menu.handle_events()
                if action == "continue":
                    self.paused = False
                elif action == "options":
                    options_menu = OptionsMenu(self.screen)  # Créer une instance du menu des options
                    options_menu.run()
                elif action == "main_menu":
                    from mainMenu import MainMenu  # Importer ici pour éviter l'import circulaire
                    main_menu = MainMenu(self.screen)  # Créer une instance du menu principal
                    main_menu.run()
                    running = False  # Terminer la boucle principale
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

            self.clock.tick(30)  # Limiter la vitesse de rafraîchissement à 30 FPS

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))  # Agrandir la fenêtre
    pygame.display.set_caption('Bow Man')

    game = Game(screen)
    game.run()
