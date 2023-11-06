import pygame
import math
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

    def player_rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_pos[0] - self.hitbox_rect.centerx)
        self.y_change_mouse_player = (self.mouse_pos[1] - self.hitbox_rect.centery)
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

        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.shoot = True
            self.is_shooting()
        else:
             self.shoot = False   

                
    def is_shooting(self):
        if self.shoot_coolddown == 0:
            self.shoow_cooldown = SHOOT_COOLDOWN
            # finish off later




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