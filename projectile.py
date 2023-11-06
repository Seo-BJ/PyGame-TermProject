import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, mouse_pos, image_path, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image if needed
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.width = width
        self.height = height
        x_diff = mouse_pos[0] - pos[0]
        y_diff = mouse_pos[1] - pos[1]
        angle = pygame.math.Vector2(x_diff, y_diff).angle_to(pygame.math.Vector2(1, 0))
        self.velocity = pygame.math.Vector2(self.speed, 0).rotate(-angle)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Return False if the projectile goes off screen to remove it
        if self.rect.right < 0 or self.rect.left > self.width or self.rect.bottom < 0 or self.rect.top > self.height:
            return False
        return True

    def draw(self, player_world_pos, surface):
        screen_x = self.rect.x - player_world_pos[0] + self.width // 2
        screen_y = self.rect.y - player_world_pos[1] + self.height // 2
        surface.blit(self.image, (screen_x, screen_y))
