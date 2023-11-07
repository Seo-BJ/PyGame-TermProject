import pygame
import player
from gameSetting import * 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, enemy_group, all_sprites_group, player):
        super().__init__(enemy_group, all_sprites_group,)
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.imgae = pygame.transform.rotozoom(self.image, 0, 2)

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.player = player
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        self.position = pygame.math.Vector2(position)

        # Enemy HP
        self.max_hp = ENEMY_MAXHP  
        self.current_hp = self.max_hp

        # Enemy Knockback
        self.knockback_duration = 0  # Duration of knockback effect
        self.knockback_velocity = pygame.math.Vector2()  # Velocity during knockback
    
    def chase_player(self):
        player_vector = pygame.math.Vector2(self.player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vetcor_length(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2() # zero vector

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y


    def get_vetcor_length(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()
    
    def take_damage(self, amount, knockback_direction=None, knockback_strength=100):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.kill()  # Remove the enemy from all groups
        else:
            # Apply knockback effect
            if knockback_direction is not None:
                self.knockback_velocity = knockback_direction.normalize() * knockback_strength
                self.knockback_duration = 120  # Number of frames to apply knockback

    def update(self):
        if self.knockback_duration > 0:
            # Apply knockback movement
            self.position += self.knockback_velocity
            self.knockback_duration -= 1
            if self.knockback_duration <= 0:
                # Reset knockback velocity
                self.knockback_velocity = pygame.math.Vector2()
        else:
            # Chase player if not in knockback
            self.chase_player()
        self.rect.center = self.position
