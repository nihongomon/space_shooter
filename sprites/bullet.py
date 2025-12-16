from config import *
from sprites.game_sprite import GameSprite


class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("Effects\\fire01.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
