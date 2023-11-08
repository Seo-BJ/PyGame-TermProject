import pygame
import spritesheet
from gameSetting import *
from enemy import Enemy

MOVE = 'move'
DIE = "die"
ATTACK = "attack"

class Witch(pygame.sprite.Sprite):
    def __init__(self, position, enemy_group, all_sprites_group, player):
        super().__init__(enemy_group, all_sprites_group)
        self.player = player
        self.position = pygame.math.Vector2(position)
        self.image =  pygame.image.load('Witch\Witch_Walk.png').convert_alpha()
        self.sprite_sheets = {
            DIE: spritesheet.SpriteSheet("DIE",'Witch\Witch_Die.png', 12, 64, 64, 3, (0,0,0)),
            MOVE: spritesheet.SpriteSheet('MOVE', 'Witch\Witch_Walk.png', 8, 64, 64, 3, (0,0,0)),
            ATTACK: spritesheet.SpriteSheet("ATTACK", 'Witch/Witch_Attack.png', 18, 64, 64, 3, (0,0,0))
        }
        self.current_state = MOVE
        self.facing_right = True
        self.current_sheets =  self.sprite_sheets[self.current_state]
        self.base_witch_image = self.current_sheets.get_base_image()

        self.rect = self.base_witch_image.get_rect(center = self.position)

        self.speed = BAT_SPEED  
        self.max_hp = BAT_HP  
        self.current_hp = self.max_hp

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()

        # Enemy Knockback
        self.knockback_duration = 0  # Duration of knockback effect
        self.knockback_velocity = pygame.math.Vector2()  # Velocity during knockback

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
        self.rect = self.base_witch_image.get_rect(center=self.rect.center)

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
        
    def apply_knockback(self, knockback_direction, knockback_strength):
        # Apply knockback effect
        self.knockback_velocity = knockback_direction.normalize() * knockback_strength
        self.knockback_duration = 15  # Number of frames to apply knockback

    def take_damage(self, amount, knockback_direction=None, knockback_strength=100):
        self.current_hp -= amount
        if self.current_hp <= 0 and self.current_state != DIE:
            self.set_animation_state(DIE)
            self.velocity = pygame.math.Vector2()  
            self.knockback_duration = 0  
        else:
            if knockback_direction is not None:
                self.apply_knockback(knockback_direction, knockback_strength)

    def die(self):
        self.player.current_exp += 15
        self.kill()

    def animate_death(self):
        if self.current_sheets.current_frame == self.current_sheets.frame_count - 1:
            self.kill()
        else:
            self.image = self.current_sheets.get_frame()
            self.rect = self.image.get_rect(center=self.rect.center)
            
    def attack_player(self):
        # This method will handle the attack logic
        # Create and add the Projectile to the appropriate groups
        # For now, let's just print a message
        print("Witch is attacking!")
        self.set_animation_state(ATTACK)
        # Create a projectile here and add it to the groups
        # projectile = Projectile(...)
        # self.projectile_group.add(projectile)
        # self.all_sprites_group.add(projectile)

    def update(self):
        player_vector = pygame.math.Vector2(self.player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_length(player_vector, enemy_vector)

        if self.current_state == DIE:
            self.animate_death()
        else:
            if distance < self.RANGE and self.current_state != ATTACK:
                self.attack_player()
            elif self.current_state == ATTACK:
                # Check if the attack animation is finished
                if self.current_sheets.current_frame == self.current_sheets.frame_count - 1:
                    self.set_animation_state(MOVE)  # Switch back to move state after attack
            else:
                self.chase_player()  # Chase player if not attacking or dying

            self.rect.center = self.position

            self.enemy_flip()
            self.animate()

