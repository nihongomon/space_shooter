import pygame

from config import *
from sprites.bullet import Bullet
from sprites.game_sprite import GameSprite


class Player(GameSprite):
    def __init__(self):
        super().__init__("playerShip1_blue.png")
        self.image = pygame.transform.scale(self.image, (50, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400 // 2
        self.rect.bottom = 600 - 10
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
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
