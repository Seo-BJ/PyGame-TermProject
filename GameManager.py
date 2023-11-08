import pygame
import random
import gameSetting
from pygame.locals import *
from player import Player
from enemy import Enemy
from projectile import Projectile
from menu import Menu
from playerUI import PlayerUI
from levelUpUI import LevelUpUI
from pauseMenu import PauseMenu
import spritesheet
from orbitobject import OrbitObject

from bat import Bat
#from enemy import *

# Initialize pygame
pygame.init()

# 디스플레이 설정
screen = pygame.display.set_mode((gameSetting.WIDTH, gameSetting.HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()


# Player settings
player_size = 50
player_pos = [gameSetting.WIDTH // 2, gameSetting.HEIGHT // 2]
player_speed = 5


# Background Image and Map
background = pygame.image.load("background.png").convert()
map_width = background.get_width()
map_height = background.get_height()



# Reset Game
def reset_game():
    # Reset player state
    player.current_hp = player.max_hp
    player.pos = pygame.math.Vector2(gameSetting.PLAYER_START)
    player.velocity_x = 0
    player.velocity_y = 0
    player.rect.center = player.pos

    # Clear all sprites from groups
    for group in [all_sprites_group, enemy_group, projectile_group]:
        for entity in group:
            entity.kill()  # This will remove the sprite from all groups

    # Reinitialize or reset other game state as necessary
    # For example, if you have a score or level system, reset it here
    # score = 0
    # level = 1



    # Reset any other game state variables here
    # ...

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft = (0, 0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - gameSetting.WIDTH // 2
        self.offset.y = player.rect.centery - gameSetting.HEIGHT // 2

        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

# Sprite Group
all_sprites_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Player, Camera
player = Player(projectile_group,all_sprites_group, enemy_group)
all_sprites_group.add(player)
camera = Camera()

########## UI & FONT ############################################################
# Font
font_size = gameSetting.FONT_SIZE  
pixel_font = pygame.font.Font('Font/Silver_font.ttf', font_size)

# UI
game_ui = PlayerUI(screen, pixel_font, player)
menu = Menu(screen, pixel_font)
pause_menu = PauseMenu(screen, menu,game_ui)
level_up_ui = LevelUpUI(player, all_sprites_group, enemy_group ,screen, pause_menu)

# Spawn Manage
# Reset the spawn timer for enemies
global last_enemy_spawn_time
last_enemy_spawn_time = pygame.time.get_ticks()
directions = gameSetting.SPAWN_DIRECTIONS

pause_reason = "ESC KeyDown"

# Game Start before the game loop
menu.start_menu()


# Game loop
running = True
while running:
    screen.fill(gameSetting.BLACK)

    # 이벤트 핸들링
    for event in pygame.event.get():
        # Quit PyGame Program
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu.toggle_pause()  
                game_ui.toggle_pause()  
                pause_reason =  "ESC KeyDown"

    # 플레이어 레벨업 이벤트
    if player.level_up():
        pause_menu.toggle_pause()  
        game_ui.toggle_pause()  
        pause_reason = "Level Up"

    # 일시정지 이벤트 
    if pause_menu.paused:
        if pause_reason ==  "ESC KeyDown":
            pause_menu.update()  
            continue
        elif pause_reason == "Level Up":
            level_up_ui.update()
            continue
            
    # 플레이어 Hit 이벤트
    hits = pygame.sprite.spritecollide(player, enemy_group, False)
    if hits:
        player.take_damage(10)  # Example damage value

    # 게임 오버 이벤트
    if player.current_hp <= 0:
        print("Player health is zero, calling game_over")  # Debugging print
        action = menu.game_over()
        print(f"Game over action: {action}")  # Debugging print
        if action == 'exit':
            running = False
        elif action == 'restart':
            reset_game()  # Reset the game state
            menu.start_menu()  # Show the start menu again
            running = True  # Set running to True to restart the game loop

    # Enemy Spawn
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > gameSetting.ENEMY_SPAWN_INTERVAL:
        last_enemy_spawn_time = current_time
        for direction in directions:
            spawn_distance = max(gameSetting.WIDTH, gameSetting.HEIGHT) * 1.5  
            spawn_position = player.pos + direction * spawn_distance
            enemy = Bat(spawn_position, enemy_group, all_sprites_group, player)

    # UI, Camera and sprite updates
    camera.custom_draw()
    all_sprites_group.update()
    game_ui.draw_allUI(player)  
    # Update the display, Cap the frame rate
    pygame.display.update()
    clock.tick(gameSetting.FPS)

     
pygame.quit()
