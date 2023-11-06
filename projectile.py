import pygame
import math
from gameSetting import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self,x, y, angle):
        super().__init__()
        self.image = pygame.image.load("projectile.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, PROJECTILE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = x
        self.y = y
        self.angle = angle
        self.speed = PROJECTILE_SPEED
        self.x_velocity = math.cos(self.angle * (2*math.pi/360))*self.speed
        self.y_velocity = math.sin(self.angle * (2*math.pi/360))*self.speed

        self.lifetime = PROJECTILE_LIFETIME
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
