import pygame
import sys
from pauseMenu import PauseMenu

class LevelUpUI:
    def __init__(self, screen, pause_menu):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        self.buttons = ["Button 1", "Button 2", "Button 3"]
        self.pause_menu = pause_menu

    def draw_button(self, text, center):
        text_render = self.font_small.render(text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=center)
        button_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
        self.screen.blit(text_render, text_rect)
        return button_rect

    def show_level_up_screen(self):
        button_rects = []
        for i, button_text in enumerate(self.buttons):
            button_rects.append(self.draw_button(button_text, (self.screen.get_width() // 2, 150 + i * 100)))

        pygame.display.flip()  # Update the display to show the buttons

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        print(f"{self.buttons[i]} was clicked")  # Placeholder for button logic
                        self.pause_menu.toggle_all()

    def update(self):
        self.show_level_up_screen()
