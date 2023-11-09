import pygame
import spritesheet
from gameSetting import *
from enemy import Enemy

MOVE = 'move'
DIE = "die"

class Bat(pygame.sprite.Sprite):
    def __init__(self, position, enemy_group, all_sprites_group, player, hit_sound):
        super().__init__(enemy_group, all_sprites_group)
        self.player = player
        self.position = pygame.math.Vector2(position)
        self.image =  pygame.image.load('Bat\Bat_Flight.png').convert_alpha()
        self.sprite_sheets = {
            DIE: spritesheet.SpriteSheet("DIE",'Bat\Bat_Die.png', 10, 64, 64, 2, (0,0,0)),
            MOVE: spritesheet.SpriteSheet('MOVE', 'Bat\Bat_Flight.png', 8, 64, 64, 2, (0,0,0)),
        }
        self.current_state = MOVE
        self.facing_right = True
        self.current_sheets =  self.sprite_sheets[self.current_state]
        self.base_bat_image = self.current_sheets.get_base_image()

        self.rect = self.base_bat_image.get_rect(center = self.position)

        self.speed = BAT_SPEED  
        self.max_hp = BAT_HP  
        self.current_hp = self.max_hp

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.hit_sound = hit_sound
        # Enemy Knockback
        self.knockback_duration = 0  
        self.knockback_velocity = pygame.math.Vector2()  

        # Bat
        self.exp = BAT_EXP

    def enemy_flip(self):
        player_x =  pygame.math.Vector2(self.player.hitbox_rect.center)[0]
        enemy_x = pygame.math.Vector2(self.rect.center)[0]
        if player_x < enemy_x:
            self.facing_right = False
        else:
            self.facing_right = True

    def set_animation_state(self, new_state):
        if self.current_state != new_state:
            self.current_state = new_state
            self.current_sheets = self.sprite_sheets[new_state]

    def animate(self):
        self.image =  self.current_sheets.get_frame()
        if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey((0, 0, 0)) 
        self.rect = self.base_bat_image.get_rect(center=self.rect.center)

    def chase_player(self):
        player_vector = pygame.math.Vector2(self.player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vetcor_length(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2() 

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vetcor_length(self, vector_1, vector_2):
            return (vector_1 - vector_2).magnitude()
        
    def apply_knockback(self, knockback_direction, knockback_strength):
        self.knockback_velocity = knockback_direction.normalize() * knockback_strength
        self.knockback_duration = 8

    def take_damage(self, amount, knockback_direction=None, knockback_strength=100):
        self.current_hp -= amount
        if self.current_hp <= 0 and self.current_state != DIE:
            self.set_animation_state(DIE)
            self.velocity = pygame.math.Vector2()  
            self.knockback_duration = 0  
        else:
            if knockback_direction is not None:
                self.apply_knockback(knockback_direction, knockback_strength)
        self.hit_sound.play()

    def die(self):
        self.player.current_exp += self.exp
        self.hit_sound.play()
        self.kill()

    def update(self):
        if self.current_state == DIE:
            self.animate_death()
    
        else:
            if self.knockback_duration > 0:
                self.position += self.knockback_velocity
                self.knockback_duration -= 1
                if self.knockback_duration <= 0:
                    self.knockback_velocity = pygame.math.Vector2()
            else:
                self.chase_player()
            self.rect.center = self.position

            self.enemy_flip()
            self.animate()

    def animate_death(self):
        if self.current_sheets.current_frame == self.current_sheets.frame_count - 1:
            self.die()
        else:
            self.image = self.current_sheets.get_frame()
            self.rect = self.image.get_rect(center=self.rect.center)