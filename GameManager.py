import pygame
import random
from pygame.locals import *
from gameSetting import *
from player import Player
from projectile import Projectile
#from enemy import *

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



# Background
background = pygame.image.load("background.png").convert()




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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.imgae = pygame.transform.rotozoom(self.image, 0, 2)

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        self.position = pygame.math.Vector2(position)
    
    def chase_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vetcor_length(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2() # zero vector

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y


    def get_vetcor_length(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()
    
    def update(self):
        self.chase_player()


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
player = Player()
camera = Camera()
enemy = Enemy((400, 400))

all_sprites_group.add(player)


# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        # Quit PyGame Program
        if event.type == pygame.QUIT:
            running = False
        # Mouse Button
        if pygame.mouse.get_pressed() == (1, 0, 0):
            player.shoot = True
            projectile = player.is_shooting()
            projectile_group.add(projectile)
            all_sprites_group.add(projectile)
        else:
            player.shoot = False   

    # screen.blit(background, (0,0))

    camera.custom_draw()
    all_sprites_group.update()


    # Update the display, Cap the frame rate
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
