import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        self.running = True

    def draw_button(self, text, center, action=None):
        text_render = self.font_small.render(text, True, WHITE)
        text_rect = text_render.get_rect(center=center)
        button_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(self.screen, GREEN if action != "Exit" else RED, button_rect)
        self.screen.blit(text_render, text_rect)
        return button_rect

    def start_menu(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            start_button = self.draw_button('Game Start', (self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
            exit_button = self.draw_button('Exit', (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50), "Exit")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.running = False
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def game_over(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return 'exit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.running = False
                        return 'restart'
                    elif exit_button.collidepoint(event.pos):
                        self.running = False
                        return 'exit'

            self.screen.fill((0, 0, 0))  # Make sure this is before drawing anything else
            self.screen.blit(self.font.render('You Died!', True, RED), (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 100))
            restart_button = self.draw_button('Restart', (self.screen.get_width() // 2, self.screen.get_height() // 2))
            exit_button = self.draw_button('Exit', (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100), "Exit")

            pygame.display.update()  # Update the display after drawing
            self.clock.tick(60)
