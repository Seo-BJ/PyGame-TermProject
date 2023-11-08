import pygame
# Game Setting
WIDTH = 1440
HEIGHT = 810
FPS = 60
GAME_TIME = 10 # 10 minute
# Player Setting
PLAYER_START = 720, 405
PLAYER_SPEED = 6
PLAYER_MAXHP = 100

PLAYER_INVINCIBLE_DURATION = 2000
PLAYER_PUSH_POWER = 100

PLAYER_LEVELUP_EXP = []
PLAYER_MAX_LEVEL = 10
PLAYER_EXP_COEFFICEINT = 0.2
GUN_OFFXET_X = 50
GUN_OFFXET_Y = 50

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
ENEMY_SPAWN_INTERVAL = 2000 # 5 seconds
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

# Bat Enemy
BAT_SPEED = 3
BAT_HP = 40
BAT_EXP = 10

# Witch Enemy
WITCH_SPEED = 1.5
WTICH_HP = 70
WTICH_EXP = 15
WITCH_RANGE = 300
WITCH_PROJECTILE_SPEED = 8
WITCH_PROJETILE_LIEFETIME = 2000
WITCH_SHOOT_COOLDOWN = 1800

# Color Setting
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font
FONT_SIZE = 64
