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
    
    def update(self):
        self.chase_player()
