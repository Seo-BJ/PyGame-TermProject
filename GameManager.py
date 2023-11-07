import pygame
import random
from pygame.locals import *
from gameSetting import *
from player import Player
from enemy import Enemy
from projectile import Projectile
from menu import Menu
#from enemy import *

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
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


# UI

def draw_health_bar(screen, pos, size, border_color, inner_color, current, max_health):
    border_rect = pygame.Rect(pos, size)
    inner_rect = pygame.Rect(pos, (size[0] * (current / max_health), size[1]))
    pygame.draw.rect(screen, border_color, border_rect, 2)  # Draw border
    pygame.draw.rect(screen, inner_color, inner_rect)  # Draw inner health bar

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

    # Reset the spawn timer for enemies
    global last_enemy_spawn_time
    last_enemy_spawn_time = pygame.time.get_ticks()

    # Add the player back to the all_sprites_group
    all_sprites_group.add(player)

    # Reset any other game state variables here
    # ...

# ... [Your existing code] ...

def generate_chunk(x, y):
    """ Generate a new chunk at the given (x, y) position """
    tiles = []
    for i in range(chunk_size // 10):
        for j in range(chunk_size // 10):
            if random.randint(0, 10) > 8:
                tiles.append((x + i * 10, y + j * 10))
    return tiles

def get_chunk_pos(x, y):
    """ Get the chunk position for the given (x, y) position """
    return x // chunk_size * chunk_size, y // chunk_size * chunk_size



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
camera = Camera()
#enemy = Enemy((400, 400))

all_sprites_group.add(player)

# Spawn Manage
last_enemy_spawn_time = pygame.time.get_ticks()

# Game Start before the game loop
menu.start_menu()
# Enemy Spawn Direction
directions = [
            pygame.math.Vector2(1, 0),  # Right
            pygame.math.Vector2(1, 1).normalize(),  # Down-Rightds
            pygame.math.Vector2(0, 1),  # Down
            pygame.math.Vector2(-1, 1).normalize(), # Down-Left
            pygame.math.Vector2(-1, 0), # Left
            pygame.math.Vector2(-1, -1).normalize(),# Up-Left
            pygame.math.Vector2(0, -1), # Up
            pygame.math.Vector2(1, -1).normalize(), # Up-Right
        ]
# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        # Quit PyGame Program
        if event.type == pygame.QUIT:
            running = False


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
            running = True  # Set running to True to restart the game loo

    # Enemy Spawn
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
        last_enemy_spawn_time = current_time
        for direction in directions:
            spawn_distance = max(WIDTH, HEIGHT) * 1.5  
            spawn_position = player.pos + direction * spawn_distance
            enemy = Enemy(spawn_position, enemy_group, all_sprites_group, player)
            #enemy_group.add(enemy)
            #all_sprites_group.add(enemy)

    # {;ayer Hit Event
    hits = pygame.sprite.spritecollide(player, enemy_group, False)
    if hits:
        player.take_damage(10)  # Example damage value
    # UI
    draw_health_bar(
        screen,
        (10, 10),  # Position of the health bar
        (200, 20),  # Size of the health bar
        (255, 0, 0),  # Color of the border (red)
        (0, 255, 0),  # Color of the inner bar (green)
        player.current_hp,
        player.max_hp
    )
    # screen.blit(background, (0,0))
    camera.custom_draw()
    all_sprites_group.update()

    # Projectile Hit Event
    for projectile in projectile_group:
        projectile.update()

    # Update the display, Cap the frame rate
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
