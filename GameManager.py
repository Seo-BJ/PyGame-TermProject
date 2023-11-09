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


from bat import Bat
from witch import Witch
#from enemy import *

# Initialize pygame
pygame.init()

# 디스플레이 설정
screen = pygame.display.set_mode((gameSetting.WIDTH, gameSetting.HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()


# Sound

hit_sound = pygame.mixer.Sound("Sound\Die.wav")
shoot_sound = pygame.mixer.Sound("Sound\Shoot.wav")
hit_sound.set_volume(0.25)
shoot_sound.set_volume(0.4)

# Background Image and Map
background = pygame.image.load("map.png").convert()

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(center = (gameSetting.WIDTH//2, gameSetting.HEIGHT//2))

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
player = Player(projectile_group,all_sprites_group, enemy_group, screen, shoot_sound)
all_sprites_group.add(player)
camera = Camera()

########## UI & FONT ############################################################
# Font
font_size = gameSetting.FONT_SIZE  
pixel_font = pygame.font.Font('Font/Silver_font.ttf', font_size)

# UI
playerUI = PlayerUI(screen, pixel_font, player)
menu = Menu(screen, pixel_font)
pause_menu = PauseMenu(screen, menu,playerUI)
level_up_ui = LevelUpUI(player,pixel_font, all_sprites_group, enemy_group ,screen, pause_menu)


# Reset the spawn timer for enemies
global last_enemy_spawn_time
last_enemy_spawn_time = pygame.time.get_ticks()
directions = gameSetting.SPAWN_DIRECTIONS

pause_reason = "ESC KeyDown"

# Game Start before the game loop
menu.start_menu()
pygame.mixer.music.load("Sound\BGM.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
start_time = pygame.time.get_ticks()

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
                playerUI.toggle_pause()  
                pause_reason =  "ESC KeyDown"

    # 플레이어 레벨업 이벤트
    if player.level_up():
        pause_menu.toggle_pause()  
        playerUI.toggle_pause()  
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
    hits = pygame.sprite.spritecollide(player, enemy_group, False,  pygame.sprite.collide_rect_ratio(0.2))
    if hits:
        player.take_damage(10) 
        playerUI.start_healthbar_blink()
        hit_sound.play()

# 게임 오버 이벤트
    if player.current_hp <= 0:
        action = menu.game_over()
        if action == 'exit':
            running = False

    minutes_passed = (pygame.time.get_ticks() - start_time) // 120000

    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > gameSetting.ENEMY_SPAWN_INTERVAL:
        last_enemy_spawn_time = current_time
        enemy_increase_factor = 1.1
        enemy_multiplier = min(enemy_increase_factor ** minutes_passed, gameSetting.MAX_ENEMY_MULTIPLIER)
        number_of_enemies = int(enemy_multiplier)  
        for _ in range(number_of_enemies):
            for direction in directions:
                spawn_distance = max(gameSetting.WIDTH, gameSetting.HEIGHT) * 1.5
                spawn_position = player.pos + direction * spawn_distance
                
                if random.choice([True, False]):
                    enemy = Witch(spawn_position, projectile_group, enemy_group, all_sprites_group, player, hit_sound)
                else:
                    enemy = Bat(spawn_position, enemy_group, all_sprites_group, player, hit_sound)

       


    
    # Update 
    camera.custom_draw()
    all_sprites_group.update()
    playerUI.draw_allUI(player)  

    pygame.display.update()
    clock.tick(gameSetting.FPS)

pygame.quit()
