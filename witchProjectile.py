import pygame
import math
from gameSetting import *

class WitchProjectile(pygame.sprite.Sprite):
    def __init__(self,x, y, angle, player):
        super().__init__()
        self.image = pygame.image.load("projectile.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.player = player
        self.x = x
        self.y = y
        self.angle = angle
        
        # Projectile Stats
        self.lifetime = WITCH_PROJETILE_LIEFETIME
        self.speed = WITCH_PROJECTILE_SPEED

        self.x_velocity = math.cos(self.angle * (2*math.pi/360))*self.speed
        self.y_velocity = math.sin(self.angle * (2*math.pi/360))*self.speed
        self.spawn_time = pygame.time.get_ticks()
        
    def projectile_movement(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def update(self):
        self.projectile_movement()

    #### 
    def push_enemies_away(self, knockback_radius, knockback_strength):
        return
    def take_damage(self, amount, knockback_direction=None, knockback_strength=100):
        return