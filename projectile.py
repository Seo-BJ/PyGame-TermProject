import pygame
import math
from gameSetting import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self,x, y, angle, enemy_group):
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

        # Projectile Stats
        self.damage = 10
        self.penetrate_count = 0  # Number of enemies penetrated
        self.max_penetrations = 2  # Maximum number of penetrations before disappearing

        self.enemy_group = enemy_group

    def projectile_movement(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

    def update(self):
        self.projectile_movement()

        hits = pygame.sprite.spritecollide(self, self.enemy_group, False)
        for enemy in hits:
            enemy.take_damage(self.damage)  # Damage the enemy
            self.penetrate_count += 1  # Increment penetration count
            if self.penetrate_count >= self.max_penetrations:
                self.kill()  # Destroy the projectile after maximum penetrations
                break  # Exit the loop after destroying the projectile
