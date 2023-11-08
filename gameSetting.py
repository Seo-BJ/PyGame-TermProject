import pygame
# Game Setting
WIDTH = 1200
HEIGHT = 900
FPS = 60
GAME_TIME = 10 # 10 minute
# Player Setting
PLAYER_START = 400, 500
PLAYER_SPEED = 6
PLAYER_MAXHP = 100

PLAYER_INVINCIBLE_DURATION = 2000
PLAYER_PUSH_POWER = 100

PLAYER_LEVELUP_EXP = []
PLAYER_MAX_LEVEL = 10
PLAYER_EXP_COEFFICEINT = 0.2
GUN_OFFXET_X = 45
GUN_OFFXET_Y = 20

ORBIT_NUM = 0
# Bullet Setting
SHOOT_COOLDOWN = 30
PROJECTILE_SCALE = 1.0
PROJECTILE_SPEED = 15
PROJECTILE_LIFETIME = 500
PROJETILE_PENETRATION = 1
PROJECTILE_DAMAGE = 20

# Enemy Setting
ENEMY_SPEED = 4
ENEMY_SPAWN_INTERVAL = 5000 # 5 seconds
ENEMY_MAXHP = 50

SPAWN_DIRECTIONS =  [
            pygame.math.Vector2(1, 0),  # Right
            pygame.math.Vector2(1, 1).normalize(),  # Down-Rightds
            pygame.math.Vector2(0, 1),  # Down
            pygame.math.Vector2(-1, 1).normalize(), # Down-Left
            pygame.math.Vector2(-1, 0), # Left
            pygame.math.Vector2(-1, -1).normalize(),# Up-Left
            pygame.math.Vector2(0, -1), # Up
            pygame.math.Vector2(1, -1).normalize(), # Up-Right
        ]
# Color Setting
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


