import pygame
import gameSetting
import random
from player import Player
from pauseMenu import PauseMenu
from orbitobject import OrbitObject

class LevelUpUI:
    def __init__(self, player, all_sprites_group, enemy_group, screen, pause_menu):
        self.player = player
        self.all_sprites_group = all_sprites_group
        self.enemy_group = enemy_group
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)
        self.pause_menu = pause_menu
        self.while_level_up = True
        self.power_up_types = [
            "Projectile_Penetration",
            "Projectile_Power",
            "Projectile_RapidFire",
            "Player_Movement"
        ]
        self.isSwoing = False
    
        
    def draw_button(self, text, center):
        text_render = self.font_small.render(text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=center)
        button_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
        self.screen.blit(text_render, text_rect)
        return button_rect
 
    def show_level_up_buttons(self):
        if not self.isSwoing:
            self.isSwoing = True
            buttons = random.sample(self.power_up_types, 3)
            button_width = 200 
            button_spacing = 100  
            total_width = (button_width * len(buttons)) + (button_spacing * (len(buttons) - 1))
            start_x = (self.screen.get_width() - total_width) // 2  # Starting X position for the first button
            button_rects = []

            for i, button_type in enumerate(buttons):
                button_text = button_type.replace("_", " ")  # Replace underscores with spaces for display
                button_x = start_x + (i * (button_width + button_spacing))  # X position for this button
                button_center = (button_x + button_width // 2, self.screen.get_height() // 2)
                button_rects.append(self.draw_button(button_text, button_center))


            pygame.display.flip()  # Update the display to show the buttons

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i, rect in enumerate(button_rects):
                            if rect.collidepoint(event.pos):
                                self.power_up(buttons[i]) 
                                waiting_for_input = False
                                self.pause_menu.toggle_all()
                                self.isSwoing = False
                                self.create_orbiting_objects(self.player, self.all_sprites_group, self.screen, 'projectile.png', 5, 1, 150)
                                break  # Break out of the loop once a button is clicked

    def power_up(self, type):
        if type == "Projectile_Penetration":
            gameSetting.PROJETILE_PENETRATION += 1
        elif type == "Projectile_Power":
            gameSetting.PROJECTILE_DAMAGE += 20
        elif type == "Projectile_RapidFire":
            gameSetting.SHOOT_COOLDOWN -= 3
        #elif type == "Player_Reload":
        elif type == "Player_Movement":
            gameSetting.PLAYER_SPEED += 2

    def create_orbiting_objects(self, player, all_sprites_group, screen, image_path, level, rotation_speed, orbit_distance):
        angle_between_objects = 360 / level
        for i in range(level):
            angle_offset = i * angle_between_objects
            orbit_object = OrbitObject(player, screen, self.enemy_group, image_path, orbit_distance, angle_offset, rotation_speed)
            all_sprites_group.add(orbit_object)

    def update(self):
        self.show_level_up_buttons()