import pygame
import math

class OrbitObject(pygame.sprite.Sprite):
    def __init__(self, player, screen, image_path, orbit_distance, angle_offset, rotation_speed):
        super().__init__()
        self.player = player
        self.screen = screen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.orbit_distance = orbit_distance
        self.angle = angle_offset  # This is the initial angle offset for the object
        self.rotation_speed = rotation_speed

    def update(self):
        # Update the angle for rotation
        self.angle = (self.angle + self.rotation_speed) % 360
        angle_rad = math.radians(self.angle)

        # Calculate the new position based on the player's position
        self.rect.centerx = self.player.pos.x + self.orbit_distance * math.cos(angle_rad)
        self.rect.centery = self.player.pos.y + self.orbit_distance * math.sin(angle_rad)

        # Rotate the image to face the player
        dx, dy = self.player.pos.x - self.rect.centerx, self.player.pos.y - self.rect.centery
        angle_to_player = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.image, -angle_to_player)
        self.rect = self.image.get_rect(center=self.rect.center)
