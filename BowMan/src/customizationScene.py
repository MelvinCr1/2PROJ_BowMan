import pygame
import os

class CustomizationScene:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.selected_background = None
        self.selected_style = None
        self.play_mode = 'local'

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, '../assets/')

        self.background_options = ['background1.jpg', 'background2.jpg']
        self.style_options = ['archer.png', 'archer2.png']
        
        self.selected_background = self.background_options[0]
        self.selected_style = self.style_options[0]

        # Load images
        self.background_images = [self.load_image(os.path.join(self.assets_path, 'backgrounds', bg), (self.width, self.height)) for bg in self.background_options]
        self.style_images = [self.load_image(os.path.join(self.assets_path, 'characters', style), (200, 400)) for style in self.style_options]

    def load_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"
                elif event.key == pygame.K_RETURN:
                    return "start_game"
                elif event.key == pygame.K_b:
                    current_index = self.background_options.index(self.selected_background)
                    self.selected_background = self.background_options[(current_index + 1) % len(self.background_options)]
                elif event.key == pygame.K_s:
                    current_index = self.style_options.index(self.selected_style)
                    self.selected_style = self.style_options[(current_index + 1) % len(self.style_options)]
                elif event.key == pygame.K_m:
                    self.play_mode = 'local' if self.play_mode == 'ai' else 'ai'
        return None

    def draw(self):
        # Draw selected background
        background_index = self.background_options.index(self.selected_background)
        self.screen.blit(self.background_images[background_index], (0, 0))

        # Draw archers in their positions
        style_index = self.style_options.index(self.selected_style)
        archer_left = self.style_images[style_index]
        archer_right = pygame.transform.flip(archer_left, True, False)

        left_position = (50, self.height // 2 - archer_left.get_height() // 2)
        right_position = (self.width - 250, self.height // 2 - archer_right.get_height() // 2)

        self.screen.blit(archer_left, left_position)
        self.screen.blit(archer_right, right_position)

        # Draw text options in the center
        font = pygame.font.Font(None, 36)
        background_text = font.render(f"Background: {self.selected_background} (Press B to change)", True, (255, 255, 255))
        style_text = font.render(f"Style: {self.selected_style} (Press S to change)", True, (255, 255, 255))
        mode_text = font.render(f"Mode: {'AI' if self.play_mode == 'ai' else 'Local'} (Press M to change)", True, (255, 255, 255))
        start_text = font.render("Press ENTER to start", True, (255, 255, 255))

        text_x = self.width // 2 - background_text.get_width() // 2
        self.screen.blit(background_text, (text_x, 50))
        self.screen.blit(style_text, (text_x, 100))
        self.screen.blit(mode_text, (text_x, 150))
        self.screen.blit(start_text, (text_x, 200))

        pygame.display.flip()

    def run(self):
        while True:
            action = self.handle_events()
            if action:
                return {
                    'action': action,
                    'selected_background': self.selected_background,
                    'selected_style': self.selected_style,
                    'play_mode': self.play_mode
                }
            self.draw()
            self.clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 800))
    pygame.display.set_caption('Bow Man')

    game = CustomizationScene(screen)
    game.run()
