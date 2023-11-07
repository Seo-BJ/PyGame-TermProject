import pygame
import sys
from menu import *
from gameSetting import *
from player import Player

class GameUI:
    def __init__(self, screen, player):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

        # start time when the game starts
        self.start_ticks = pygame.time.get_ticks()  
        self.total_time = GAME_TIME * (60 * 1000) 

        self.player_current_hp = player.current_hp
        self.player_max_hp = player.max_hp

        # 경험치 Bar properties
        self.player_current_exp = player.current_exp  # You need to track this in the player class
        self.player_max_exp = player.max_exp  # You need to set this in the player class

    def update_timer(self):
        # Calculate how much time is left
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        time_left = self.total_time - elapsed_time

        # Convert time left into minutes and seconds
        minutes = time_left // (60 * 1000)
        seconds = (time_left // 1000) % 60

        # Format the time string
        time_string = '{:02}:{:02}'.format(int(minutes), int(seconds))

        # Render the time string and display it on the screen
        text_render = self.font.render(time_string, True, WHITE)
        text_rect = text_render.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(text_render, text_rect)

        # Check if the time is up and end the game if it is
        if time_left <= 0:
            return 'time_up'  # You can use this return value to trigger the game over sequence

    def draw_timer(self):
        # Call this method every frame to update and draw the timer
        time_up = self.update_timer()
        if time_up == 'time_up':
            # If time is up, call the game over function from the menu
            menu = Menu(self.screen)
            menu.game_over()

  
    def health_bar(self, screen, pos, size, border_color, inner_color, current, max_health):
        border_rect = pygame.Rect(pos, size)
        inner_rect = pygame.Rect(pos, (size[0] * (current / max_health), size[1]))
        pygame.draw.rect(screen, border_color, border_rect, 2)  # Draw border
        pygame.draw.rect(screen, inner_color, inner_rect)  # Draw inner health bar
    
    def draw_health_bar(self):
        self.health_bar(self.screen,
        (10, 20),  # Position of the health bar
        (200, 10),  # Size of the health bar
        (255, 0, 0),  # Color of the border (red)
        (0, 255, 0),  # Color of the inner bar (green)
        self.player_current_hp,
        self.player_max_hp
    )

    def draw_exp_bar(self):
        print(self.player_current_exp / self.player_max_exp)
        print(self.player_current_exp)
        exp_bar_width = (self.player_current_exp / self.player_max_exp) * self.screen.get_width()
        exp_bar_height = 10  # Height of the EXP bar
        border_rect = pygame.Rect(0, 0, self.screen.get_width(), exp_bar_height)
        inner_rect = pygame.Rect(0, 0, exp_bar_width, exp_bar_height)

        # Draw the EXP bar
        pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2)  # Draw border
        pygame.draw.rect(self.screen, (0, 255, 0), inner_rect)  # Draw inner EXP bar
  
    
    def draw_allUI(self, player):
        self.player_current_hp = player.current_hp
        self.player_max_hp = player.max_hp
        self.player_current_exp = player.current_exp
        self.player_max_exp = player.max_exp  
        self.draw_exp_bar()
        self.draw_health_bar()
        self.draw_timer()
    


  