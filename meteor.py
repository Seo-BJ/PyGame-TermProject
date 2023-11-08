import pygame
import math
import gameSetting
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, target_x, target_y, enemy_group, knockback_intensity=10):
        super().__init__()
        self.image = pygame.image.load("projectile.png").convert_alpha()  # Assuming you have a meteor image
        self.image = pygame.transform.rotozoom(self.image, 0, gameSetting.PROJECTILE_SCALE)
        self.rect = self.image.get_rect()

        # Start above the screen at a random x position
        start_x = random.randint(0, gameSetting.WIDTH)
        start_y = -self.rect.height  # Start just above the screen

        self.rect.center = (start_x, start_y)

        self.target_x = target_x
        self.target_y = target_y

        # Calculate the angle to be between 60 and 90 degrees from the vertical
        angle_range = (math.radians(60), math.radians(90))
        self.angle = random.uniform(*angle_range)

        # Adjust the angle based on which side of the screen the meteor starts from
        if start_x > gameSetting.WIDTH / 2:
            self.angle = math.pi - self.angle  # Adjust for right side

        # Projectile Stats
        self.lifetime = gameSetting.PROJECTILE_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.damage = gameSetting.PROJECTILE_DAMAGE
        self.speed = gameSetting.PROJECTILE_SPEED
        self.knockback_intensity = knockback_intensity

        # Calculate velocity to move towards the target
        self.x_velocity = math.cos(self.angle) * self.speed
        self.y_velocity = math.sin(self.angle) * self.speed  # Positive to move downwards

        # Group Initialize
        self.enemy_group = enemy_group

    def update(self):
        # Move the meteor
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

        # Check if the meteor has reached its target or if its lifetime has expired
        if (self.rect.y <= self.target_y and self.y_velocity > 0) :
           ##(pygame.time.get_ticks() - self.spawn_time > self.lifetime):
            self.kill()  # Remove the meteor

        # Check for collision with enemies
        hits = pygame.sprite.spritecollide(self, self.enemy_group, False)
        for enemy in hits:
            knockback_direction = pygame.math.Vector2(self.x_velocity, self.y_velocity).normalize()
            enemy.take_damage(self.damage, knockback_direction, self.knockback_intensity)
            ##self.kill()  # Remove the meteor after hitting an enemy
