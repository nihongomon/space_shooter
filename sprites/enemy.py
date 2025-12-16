import random

import pygame

from config import *

from sprites.game_sprite import GameSprite


class Enemy(GameSprite):
    def __init__(self):
        super().__init__("Enemies\enemyBlack1.png")
        self.image = pygame.transform.scale(self.image, (40, 30))  # Resize
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
