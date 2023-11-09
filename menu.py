import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_button(self, text, center, action=None):
        text_render = self.font.render(text, True, WHITE)  # True to enable anti-aliasing
        text_rect = text_render.get_rect(center=center)
        self.screen.blit(text_render, text_rect)  # Draw text without a button background
        return text_rect

    def draw_title(self, text, center):
        text_render = self.font.render(text, True, WHITE)  # True for anti-aliasing
        text_rect = text_render.get_rect(center=center)
        self.screen.blit(text_render, text_rect)

    def start_menu(self):
        title_y_offset = -100  # Adjust this value to move the title up or down
        button_spacing = 100   # Space between the buttons

        while self.running:
            self.screen.fill((0, 0, 0))
            # Draw the title a bit higher than center
            self.draw_title('Survivor the Darkness', (self.screen.get_width() // 2, self.screen.get_height() // 2 + title_y_offset))
            # Draw buttons with the specified spacing
            start_button = self.draw_button('게임 시작', (self.screen.get_width() // 2, self.screen.get_height() // 2 + button_spacing))
            exit_button = self.draw_button('게임 종료', (self.screen.get_width() // 2, self.screen.get_height() // 2 + button_spacing * 2))

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
                    exit_button.collidepoint(event.pos)
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    return 'exit'

            self.screen.fill((0, 0, 0))  # Make sure this is before drawing anything else
            self.screen.blit(self.font.render('게임 오버!', True, RED), (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 100))
            exit_button = self.draw_button('게임 종료', (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100), "Exit")

            pygame.display.update()  # Update the display after drawing
            self.clock.tick(60)