import pygame

from config import *
from sprites.bullet import Bullet
from sprites.game_sprite import GameSprite


class Player(GameSprite):
    def __init__(self):
        super().__init__("playerShip1_blue.png")
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 38))
        
        self.base_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.hit_flash_until = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return Bullet(self.rect.centerx, self.rect.top)
        return None
    
    # 🔴 call this when player gets hit
    def trigger_hit_flash(self, duration_ms=1000):
        self.hit_flash_until = pygame.time.get_ticks() + duration_ms

    def apply_visual_effects(self, invincible: bool):
        now = pygame.time.get_ticks()

        # Start from clean sprite
        self.image = self.base_image.copy()

        # 🔴 Red hit flash (no box)
        if now < self.hit_flash_until:
            self.image.fill((255, 80, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)

        # 👻 Invincibility blink (optional)
        elif invincible:
            if (now // 100) % 2 == 0:
                self.image.set_alpha(80)
            else:
                self.image.set_alpha(200)
        else:
            self.image.set_alpha(255)

        # Keep position stable
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
