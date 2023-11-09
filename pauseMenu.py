import pygame
import sys
from gameSetting import *

class PauseMenu:
    def __init__(self, screen, menu, game_ui):
        self.screen = screen
        self.menu = menu  
        self.font = menu.font
        self.paused = False
        self.game_ui = game_ui

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_all(self):
        self.toggle_pause()
        self.game_ui.toggle_pause()
        
    def show_pause_screen(self):
       
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)  
        overlay.fill((0, 0, 0))  
        self.screen.blit(overlay, (0, 0))

        text = self.font.render('일시 정지', True, WHITE)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(text, text_rect)

        resume_button = self.menu.draw_button('게임 재개', (self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        exit_button = self.menu.draw_button('게임 종료', (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50), "Exit")
        
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
