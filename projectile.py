import pygame
import math
import gameSetting

class Projectile(pygame.sprite.Sprite):
    def __init__(self,x, y, angle, enemy_group, knockback_intensity=10):
        super().__init__()
        self.image = pygame.image.load("projectile.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, gameSetting.PROJECTILE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = x
        self.y = y
        self.angle = angle
        
        # Projectile Stats
        self.lifetime = gameSetting.PROJECTILE_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.damage = gameSetting.PROJECTILE_DAMAGE
        self.penetrate_count = 0  
        self.max_penetrations = gameSetting.PROJETILE_PENETRATION  
        self.speed = gameSetting.PROJECTILE_SPEED
        self.knockback_intensity = knockback_intensity

        self.x_velocity = math.cos(self.angle * (2*math.pi/360))*self.speed
        self.y_velocity = math.sin(self.angle * (2*math.pi/360))*self.speed

        # Group Initialize
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
            knockback_direction = pygame.math.Vector2()
            knockback_direction.x = math.cos(math.radians(self.angle))
            knockback_direction.y = math.sin(math.radians(self.angle))

            enemy.take_damage(self.damage, knockback_direction, self.knockback_intensity)  
            self.penetrate_count += 1  
            if self.penetrate_count >= self.max_penetrations:
                self.kill()  
                break  
        
