import pygame
import math
import gameSetting

class OrbitObject(pygame.sprite.Sprite):
    def __init__(self, player, screen, enemy_group, image_path, orbit_distance, angle_offset, rotation_speed):
        super().__init__()
        self.player = player
        self.screen = screen
        self.enemy_group = enemy_group
        self.image = pygame.image.load(image_path).convert_alpha()
        self.damage = gameSetting.PROJECTILE_DAMAGE 
        self.knockback_intensity = 10
        self.rect = self.image.get_rect()
        self.orbit_distance = orbit_distance
        self.angle = angle_offset  # This is the initial angle offset for the object
        self.rotation_speed = rotation_speed
    
    def update(self):
        # Update the angle for rotation
        self.angle = (self.angle + self.rotation_speed) % 360
        angle_rad = math.radians(self.angle)

        # Calculate the new position based on the player's position
        self.rect.x = self.player.pos.x + self.orbit_distance * math.cos(angle_rad)
        self.rect.y = self.player.pos.y + self.orbit_distance * math.sin(angle_rad)

        hits = pygame.sprite.spritecollide(self, self.enemy_group, False)
        for enemy in hits:
            knockback_direction = pygame.math.Vector2()
            knockback_direction.x = math.cos(math.radians(self.angle))
            knockback_direction.y = math.sin(math.radians(self.angle))
            enemy.take_damage(self.damage, knockback_direction, self.knockback_intensity)  
       
   
