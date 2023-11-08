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

        # 경험치 Bar 
        self.player_current_exp = player.current_exp  # You need to track this in the player class
        self.player_max_exp = player.max_exp  # You need to set this in the player class
        self.exp_bar_height = 20

        # 체력 Bar
        self.healthbar_blinking = False
        self.healthbar_blink_duration = PLAYER_INVINCIBLE_DURATION  
        self.healthbar_blink_interval = 100  
        self.healthbar_blink_timer = 0
        self.healthbar_blink_start_time = 0

    ########## TIMER Methods #############################################################################

    def update_timer(self):
        
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        time_left = self.total_time - elapsed_time

        minutes = time_left // (60 * 1000)
        seconds = (time_left // 1000) % 60
        timer_y_position = 80
        time_string = '{:02}:{:02}'.format(int(minutes), int(seconds))

        text_render = self.font.render(time_string, True, WHITE)
        text_rect = text_render.get_rect(center=(self.screen.get_width() // 2, timer_y_position))
        self.screen.blit(text_render, text_rect)
        if time_left <= 0:
            return 'time_up' 

    def draw_timer(self):
        time_up = self.update_timer()
        if time_up == 'time_up':
            menu = Menu(self.screen)
            menu.game_over()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.paused_ticks = pygame.time.get_ticks() 
        else:
            self.start_ticks += pygame.time.get_ticks() - self.paused_ticks

    ######################################################################################################

    ########## Health Bar Methods #############################################################################
    def health_bar(self, screen, pos, size, border_color, inner_color, current, max_health):
        border_rect = pygame.Rect(pos, size)
        inner_rect = pygame.Rect(pos, (size[0] * (current / max_health), size[1]))
        pygame.draw.rect(screen, border_color, border_rect, 2)  # Draw border
        pygame.draw.rect(screen, inner_color, inner_rect)  # Draw inner health bar
    
    def draw_exp_bar(self):
        exp_bar_width = (self.player_current_exp / self.player_max_exp) * self.screen.get_width()
        border_rect = pygame.Rect(0, 0, self.screen.get_width(), self.exp_bar_height)
        inner_rect = pygame.Rect(0, 0, exp_bar_width, self.exp_bar_height)

        # Draw the EXP bar
        pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 2)  
        pygame.draw.rect(self.screen, (0, 255, 0), inner_rect)  

    def draw_health_bar(self):
        if not self.healthbar_blinking or (pygame.time.get_ticks() - self.healthbar_blink_start_time) // self.healthbar_blink_interval % 2 == 0:
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
     # Add a method to start the health bar blinking
    def start_healthbar_blink(self):
        self.healthbar_blinking = True
        self.healthbar_blink_start_time = pygame.time.get_ticks()

    # Add a method to update the health bar blink effect
    def update_healthbar_blink(self):
        if self.healthbar_blinking:
            current_time = pygame.time.get_ticks()
            if current_time - self.healthbar_blink_start_time > self.healthbar_blink_duration:
                self.healthbar_blinking = False

    ######################################################################################################
    def draw_allUI(self, player):
        self.player_current_hp = player.current_hp
        self.player_max_hp = player.max_hp
        self.player_current_exp = player.current_exp
        self.player_max_exp = player.max_exp  

        self.update_healthbar_blink()
        self.draw_exp_bar()
        self.draw_health_bar()
        self.draw_timer()
    


  