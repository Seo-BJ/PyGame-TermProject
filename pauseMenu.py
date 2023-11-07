import pygame
import sys
from gameSetting import *

class PauseMenu:
    def __init__(self, screen, menu, game_ui):
        self.screen = screen
        self.menu = menu  # Pass the Menu instance to PauseMenu
        self.font = pygame.font.Font(None, 74)
        self.paused = False
        self.game_ui = game_ui

    def toggle_pause(self):
        self.paused = not self.paused

    def show_pause_screen(self):
        # Dim the screen or display a pause menu background
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)  # Transparency value: 0 is fully transparent, 255 is fully opaque
        overlay.fill((0, 0, 0))  # Black overlay
        self.screen.blit(overlay, (0, 0))

        # Display pause text
        text = self.font.render('Paused', True, WHITE)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(text, text_rect)

        # Draw buttons
        resume_button = self.menu.draw_button('Resume Game', (self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        exit_button = self.menu.draw_button('Exit', (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50), "Exit")

        # Event handling for buttons
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                    self.game_ui.toggle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    self.toggle_pause()
                    self.game_ui.toggle_pause()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
                self.game_ui.toggle_pause()

    def update(self):
        if self.paused:
            self.show_pause_screen()
