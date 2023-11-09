import pygame
import gameSetting
import random
from player import Player
from pauseMenu import PauseMenu


class LevelUpUI:
    def __init__(self, player, font, all_sprites_group, enemy_group, screen, pause_menu):
        self.player = player
        self.font = font
        self.all_sprites_group = all_sprites_group
        self.enemy_group = enemy_group
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.pause_menu = pause_menu
        self.while_level_up = True
        self.power_up_types = [
            "관통 + 2",
            "데미지 + 10",
            "체력 회복 및 최대 체력 증가" ,
            "에너지볼트 발사 개수 +1",
            "에너지볼트 크기 증가",
            "에너지볼트 속도 증가",
            "피격 후 무적 시간 0.5초 증가"
        ]
        self.isSwoing = False
    
        
    def draw_button(self, text, center):
        text_render = self.font.render(text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=center)
        self.screen.blit(text_render, text_rect)
        return text_rect
 
    def show_level_up_buttons(self):
        if not self.isSwoing:
            self.isSwoing = True
            buttons = random.sample(self.power_up_types, 3)
            button_height = 50  
            button_spacing = 20  
            total_height = (button_height * len(buttons)) + (button_spacing * (len(buttons) - 1))
            start_y = (self.screen.get_height() - total_height) // 2  
            button_rects = []

            for i, button_type in enumerate(buttons):
                button_text = button_type.replace("_", " ") 
                button_y = start_y + (i * (button_height + button_spacing)) 
                button_center = (self.screen.get_width() // 2, button_y + button_height // 2)
                button_rects.append(self.draw_button(button_text, button_center))

            pygame.display.flip()  

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
                                break  

    def power_up(self, type):
        if type == "관통 + 2":
            gameSetting.PROJETILE_PENETRATION += 1
        elif type == "데미지 + 10":
            gameSetting.PROJECTILE_DAMAGE += 10
        elif type == "체력 회복 및 최대 체력 증가" : 
            self.player.heal()
        elif type == "에너지볼트 발사 개수 +1":
            gameSetting.PROJECTILE_NUM += 1
        elif type == "에너지볼트 크기 증가":
            gameSetting.PROJECTILE_SCALE += 0.5
        elif type == "에너지볼트 속도 증가":
            gameSetting.PROJECTILE_SPEED += 2
        elif type == "피격 후 무적 시간 0.5초 증가":
            gameSetting.PLAYER_INVINCIBLE_DURATION +=0.5



    def update(self):
        self.show_level_up_buttons()