import pygame
import math
import random
import spritesheet
from meteor import Meteor
from orbitobject import OrbitObject
from projectile import Projectile
from gameSetting import *

IDLE = "idle"
WALKING = 'walking'

class Player(pygame.sprite.Sprite):
    def __init__(self, projectile_group, all_sprites_group, enemy_group):
        super().__init__(all_sprites_group)
        self.pos = pygame.math.Vector2(PLAYER_START[0], PLAYER_START[1])

        # 플레이어 이미지, 스프라이트
        self.image =  pygame.image.load('playerSprite\walk.png').convert_alpha()
        self.sprite_sheets = {
            IDLE: spritesheet.SpriteSheet("IDLE",'playerSprite/idle.png', 10, 96, 96, 2, (0,0,0)),
            WALKING: spritesheet.SpriteSheet("WALKING",'playerSprite/walk.png', 10, 96, 96, 2, (0,0,0)),
            #SHOOTING: spritesheet.SpriteSheet('playerSprite/shoot.png', animation_steps, 96, 96, 2, (0,0,0))
        }
        self.current_state = IDLE
        self.current_sheets =  self.sprite_sheets[self.current_state]
        self.base_player_image = self.current_sheets.get_base_image()

        hitbox_width = self.image.get_width() 
        hitbox_height = self.image.get_height() 
        self.hitbox_rect = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox_rect.center = self.pos
        self.rect = self.hitbox_rect.copy()

        # 플레이어 이동
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed_reduction_coefficient = 0.5

        # 플레이어 에니메이션
        self.facing_right = True

        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = SHOOT_COOLDOWN

        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFXET_X, GUN_OFFXET_Y)
      

        # Group Initialize
        self.projectile_group = projectile_group
        self.all_sprites_group = all_sprites_group
        self.enemy_group = enemy_group

        # 플레이어 HP
        self.max_hp = PLAYER_MAXHP
        self.current_hp = self.max_hp

        # 플레이어 무적
        self.invincible = False
        self.invincible_time = 0
        self.invincible_duration = PLAYER_INVINCIBLE_DURATION 

   

        # 플레이어 경험치(EXP) & 레벨
        self.level = 1
        self.current_exp = 0

        LAYER_LEVELUP_EXP = []
        for level in range(1, PLAYER_MAX_LEVEL + 1):
            exp = 100* PLAYER_EXP_COEFFICEINT * (level ** 2) 
            PLAYER_LEVELUP_EXP.append(exp)

        self.max_exp = PLAYER_LEVELUP_EXP[0]

     
    # 플레이어 회전 
    def player_rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_pos[0] - WIDTH // 2)
        self.y_change_mouse_player = (self.mouse_pos[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))

    # 플레이어 이미지 방향
    def player_flip(self):
        mouse_x, _ = pygame.mouse.get_pos()
        center_x = WIDTH//2
        if mouse_x < center_x:
            self.facing_right = False
        else:
            self.facing_right = True

    # 플레이어 입력 처리
    def user_Input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        if pygame.mouse.get_pressed() == (1, 0, 0):
            speed_modifier = self.speed_reduction_coefficient
            if  self.shoot_cooldown == 0:
                self.is_shooting()
                self.shoot = True
        else:
            self.shoot = False   
            speed_modifier = 1

        # 수평 수직 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if -1520 <= self.pos.y:
                self.velocity_y -= self.speed * speed_modifier
        if keys[pygame.K_s]:
            if self.pos.y <= 2320:
                self.velocity_y += self.speed * speed_modifier
        if keys[pygame.K_a]:
            if -1200 <= self.pos.x:
                self.velocity_x -= self.speed * speed_modifier
        if keys[pygame.K_d]:
            if   self.pos.x <= 2620:
                self.velocity_x += self.speed * speed_modifier

        # 대각선 이동
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_y /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)


        # 에니메이션 출력
        if self.velocity_x == 0 and  self.velocity_y == 0:
            self.set_animation_state(IDLE)
        else:
            self.set_animation_state(WALKING)

    # 플레이어 Move
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
            
    # 플레이어 Shoot State
    def is_shooting(self, num_projectiles=10, spread_angle=10):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            start_angle = -spread_angle * (num_projectiles - 1) / 2
            for i in range(num_projectiles):
                angle = self.angle + start_angle + i * spread_angle
                projectile = Projectile(self.pos[0], self.pos[1], angle, self.enemy_group, self)
                self.projectile_group.add(projectile)
                self.all_sprites_group.add(projectile)

            target_x = random.randint(-WIDTH//2, WIDTH//2)
            target_y = random.randint(-HEIGHT//2, HEIGHT//2)
            meteorite = Meteor(target_x, target_y, self.enemy_group)
            self.all_sprites_group.add(meteorite)


    # 플레이어 데미지 
    def take_damage(self, amount):
        if not self.invincible:
            self.current_hp -= amount
            if self.current_hp <= 0:
                self.current_hp = 0
            else:
                self.invincible = True
                self.invincible_time = pygame.time.get_ticks()
        
            self.push_enemies_away(knockback_radius=100, knockback_strength=10)


    # 플레이어가 적과 부딪히면 주변 적들을 잠깐 밀침
    def push_enemies_away(self, knockback_radius, knockback_strength):
        for enemy in self.enemy_group:
            player_center = pygame.math.Vector2(self.rect.center)
            enemy_center = pygame.math.Vector2(enemy.rect.center)
            direction = enemy_center - player_center

            if direction.length() == 0:  # Avoid division by zero
                continue

            if direction.length() <= knockback_radius:
                enemy.take_damage(0, direction, knockback_strength)  

    # 플레이어 레벨 업
    def level_up(self):
        if self.current_exp >= self.max_exp:
            self.current_exp = 0
            self.level += 1
            self.max_exp = PLAYER_LEVELUP_EXP[self.level -1]
            return True
        
    # 플레이어 에니메이션
    def set_animation_state(self, new_state):
        if self.current_state != new_state:
            self.current_state = new_state
            self.current_sheets = self.sprite_sheets[new_state]

    def animate(self):
        self.image =  self.current_sheets.get_frame()
        if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey((0, 0, 0)) 
        self.rect = self.base_player_image.get_rect(center=self.hitbox_rect.center)



    # 플레이어 Update
    def update(self):
        self.user_Input()
        self.move()
        self.player_flip()

        self.player_rotation()
        self.animate()
     
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invincible and pygame.time.get_ticks() - self.invincible_time > self.invincible_duration:
            self.invincible = False
