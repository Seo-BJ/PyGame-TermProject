import pygame
import sys
from menu import *
from gameSetting import *
from player import Player

class PlayerUI:
    def __init__(self, screen, font, player):
        self.screen = screen
        self.font = font

        # 타이머 UI
        self.start_ticks = pygame.time.get_ticks()  
        self.total_time = GAME_TIME * (60 * 1000) 

        self.player_current_hp = player.current_hp
        self.player_max_hp = player.max_hp

        self.is_paused = False

        # 경험치 Bar properties
        self.player_current_exp = player.current_exp  # You need to track this in the player class
        self.player_max_exp = player.max_exp  # You need to set this in the player class
        self.exp_bar_height = 20
    
    ########## TIMER Methods #############################################################################

    def update_timer(self):
        
        # Calculate how much time is left
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        time_left = self.total_time - elapsed_time

        # Convert time left into minutes and seconds
        minutes = time_left // (60 * 1000)
        seconds = (time_left // 1000) % 60
        timer_y_position = 80
        time_string = '{:02}:{:02}'.format(int(minutes), int(seconds))

        # Render the time string and display it on the screen
        text_render = self.font.render(time_string, True, WHITE)
        text_rect = text_render.get_rect(center=(self.screen.get_width() // 2, timer_y_position))
        self.screen.blit(text_render, text_rect)
        # Check if the time is up and end the game if it is
        if time_left <= 0:
            return 'time_up'  # You can use this return value to trigger the game over sequence

    def draw_timer(self):
        time_up = self.update_timer()
        if time_up == 'time_up':
            menu = Menu(self.screen)
            menu.game_over()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.paused_ticks = pygame.time.get_ticks()  # Save the time when the game is paused
        else:
            # Adjust the start_ticks to account for the pause duration
            self.start_ticks += pygame.time.get_ticks() - self.paused_ticks

    ######################################################################################################

    ########## Health UI Methods #############################################################################
    def health_bar(self, screen, pos, size, border_color, inner_color, current, max_health):
        border_rect = pygame.Rect(pos, size)
        inner_rect = pygame.Rect(pos, (size[0] * (current / max_health), size[1]))
        pygame.draw.rect(screen, border_color, border_rect, 2)  # Draw border
        pygame.draw.rect(screen, inner_color, inner_rect)  # Draw inner health bar
    
    def draw_exp_bar(self):
        # The EXP bar is at the top of the screen
        exp_bar_width = (self.player_current_exp / self.player_max_exp) * self.screen.get_width()
        border_rect = pygame.Rect(0, 0, self.screen.get_width(), self.exp_bar_height)
        inner_rect = pygame.Rect(0, 0, exp_bar_width, self.exp_bar_height)

        # Draw the EXP bar
        pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2)  
        pygame.draw.rect(self.screen, (0, 255, 0), inner_rect)  
    def draw_health_bar(self):
        # Position the health bar below the EXP bar with the same vertical distance as the timer
        health_bar_y_position = self.exp_bar_height + 20  # Adjust this value if necessary
        health_bar_width = self.screen.get_width() // 5  # One-fifth of the screen width
        self.health_bar(self.screen,
            (10, health_bar_y_position),  # Position to the left with the same horizontal margin
            (health_bar_width, 20),  # Double the height of the health bar
            (255, 0, 0),  # Color of the border (red)
            (0, 255, 0),  # Color of the inner bar (green)
            self.player_current_hp,
            self.player_max_hp
        )


    
    ######################################################################################################
    def draw_allUI(self, player):
        self.player_current_hp = player.current_hp
        self.player_max_hp = player.max_hp
        self.player_current_exp = player.current_exp
        self.player_max_exp = player.max_exp  
        
        self.draw_exp_bar()
        self.draw_health_bar()
        self.draw_timer()
    


  