import pygame
import random
from pygame.locals import *
from gameSetting import *
from player import Player
from enemy import Enemy
from projectile import Projectile
from menu import Menu
from gameUI import GameUI
from levelUpUI import LevelUpUI
from pauseMenu import PauseMenu

#from enemy import *

# Initialize pygame
pygame.init()

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

# Create Menu instance and start with the main menu
menu = Menu(screen)
menu.start_menu()

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Map settings
chunk_size = 400  # Size of a single chunk
map_chunks = {}   # Dictionary to store chunks

# Projectile 
projectiles = []
PROJECTILE_IMAGE_PATH = 'projectile.png'

# Background
background = pygame.image.load("background.png").convert()



# Reset Game
def reset_game():
    # Reset player state
    player.current_hp = player.max_hp
    player.pos = pygame.math.Vector2(PLAYER_START)
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
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

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


# UI
game_ui = GameUI(screen, player)
menu = Menu(screen)
pause_menu = PauseMenu(screen, menu,game_ui)
level_up_ui = LevelUpUI(screen, pause_menu)

# Spawn Manage
# Reset the spawn timer for enemies
global last_enemy_spawn_time
last_enemy_spawn_time = pygame.time.get_ticks()
directions = SPAWN_DIRECTIONS

# Game Start before the game loop


pause_reason = "ESC KeyDown"


menu.start_menu()
# Game loop
running = True
while running:
    screen.fill(BLACK)

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

    # 일시정지 이벤트 핸들링
    if pause_menu.paused:
        if pause_reason ==  "ESC KeyDown":
            pause_menu.update()
            continue  
        elif pause_reason == "Level Up":
            level_up_ui.update()
            continue
        


    # Game Over Event
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
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
        last_enemy_spawn_time = current_time
        for direction in directions:
            spawn_distance = max(WIDTH, HEIGHT) * 1.5  
            spawn_position = player.pos + direction * spawn_distance
            enemy = Enemy(spawn_position, enemy_group, all_sprites_group, player)

    # Player Hit Event
    hits = pygame.sprite.spritecollide(player, enemy_group, False)
    if hits:
        player.take_damage(10)  # Example damage value

    # UI
    game_ui.draw_allUI(player)

    # Camera and sprite updates
    camera.custom_draw()
    all_sprites_group.update()

    # Projectile Hit Event
    for projectile in projectile_group:
        projectile.update()

    # Update the display, Cap the frame rate
    pygame.display.update()
    clock.tick(FPS)

     
pygame.quit()
