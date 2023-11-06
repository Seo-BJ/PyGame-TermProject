import pygame
import random
from pygame.locals import *
from gameSetting import *
from player import Player
from projectile import Projectile

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

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

# Player
player = Player()

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

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        # Quit PyGame Program
        if event.type == pygame.QUIT:
            running = False
        # Mouse Button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Translate viewport position to world position
                world_x = event.pos[0] - WIDTH // 2 + player_pos[0]
                world_y = event.pos[1] - HEIGHT // 2 + player_pos[1]
                projectiles.append(Projectile(player_pos.copy(), pygame.mouse.get_pos(), PROJECTILE_IMAGE_PATH, WIDTH, HEIGHT))

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                # Translate viewport position to world position
                world_x = event.pos[0] - WIDTH // 2 + player_pos[0]
                world_y = event.pos[1] - HEIGHT // 2 + player_pos[1]
                # print("Mouse left button released at world position", (world_x, world_y))

    screen.blit(player.image, player.rect)
    player.update()
    pygame.draw.rect(screen, "red", player.hitbox_rect, width = 2)
    pygame.draw.rect(screen, "yellow", player.rect, width = 2)

    # Update projectiles
    projectiles = [proj for proj in projectiles if proj.update()]

    # Draw projectiles
    for proj in projectiles:
        proj.draw(player_pos.copy(), screen)
    
   

    # Draw the player
    # pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2, player_size, player_size))

    # Update the display, Cap the frame rate
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
