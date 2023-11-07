import pygame
import math
from projectile import *
from gameSetting import *

class Player(pygame.sprite.Sprite):
    def __init__(self, projectile_group, all_sprites_group, enemy_group):
        super().__init__(all_sprites_group)
        self.pos = pygame.math.Vector2(PLAYER_START[0], PLAYER_START[1])
        self.image = pygame.image.load("player.png").convert_alpha()
        self.base_player_image = self.image

        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
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

        # 플레이어 경험치(EXP)
        self.current_exp = 0
        self.max_exp = 100 # MUST MODIFY

    # 플레이어 회전
    def player_rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_pos[0] - WIDTH // 2)
        self.y_change_mouse_player = (self.mouse_pos[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    # 플레이어 입력 처리
    def user_Input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        # Player vertical/horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity_y -= self.speed
        if keys[pygame.K_s]:
            self.velocity_y += self.speed
        if keys[pygame.K_a]:
            self.velocity_x -= self.speed
        if keys[pygame.K_d]:
            self.velocity_x += self.speed

        # Player diagonally movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_y /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0) and self.shoot_cooldown == 0:
            self.is_shooting()
            self.shoot = True
        else:
            self.shoot = False   

    # 플레이어 Shoot State
    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_projectile_pos = self.pos + self.gun_barrel_offset.rotate(-self.angle)
            projectile = Projectile(spawn_projectile_pos[0], spawn_projectile_pos[1], self.angle, self.enemy_group)
            self.projectile_group.add(projectile)
            self.all_sprites_group.add(projectile)

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
                enemy.take_damage(0, direction, knockback_strength)  # Apply knockback without dealing damage

    # 플레이어 Move
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_Input()
        self.move()
        self.player_rotation()
        #print(self.current_exp)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.invincible and pygame.time.get_ticks() - self.invincible_time > self.invincible_duration:
            self.invincible = False