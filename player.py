import pygame
import math
from projectile import *
from gameSetting import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START[0], PLAYER_START[1])
        self.image = pygame.image.load("player.png").convert_alpha()
        self.base_player_image = self.image

        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED

        self.shoot = False
        self.shoot_cooldown = 0

        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFXET_X, GUN_OFFXET_Y)

        # Player HP
        self.max_hp = PLAYER_MAXHP
        self.current_hp = self.max_hp

    def player_rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_pos[0] - WIDTH // 2)
        self.y_change_mouse_player = (self.mouse_pos[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def user_Input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        # Player vertical/horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity_y -= self.speed
        if keys[pygame.K_s]:
            self.velocity_y += self.speed
        if keys[pygame.K_a]:
            self.velocity_x -= self.speed
        if keys[pygame.K_d]:
            self.velocity_x += self.speed

        # Player diagonally movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_y /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)


                
    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoow_cooldown = SHOOT_COOLDOWN
            spawn_projectile_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.projectile = Projectile(spawn_projectile_pos[0], spawn_projectile_pos[1], self.angle)

            return self.projectile
        
    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_Input()
        self.move()
        self.player_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1