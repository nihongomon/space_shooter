import os
import random

import pygame

from config import *
from sprites.enemy import Enemy
from sprites.player import Player


class GameManager:
    def __init__(self):

        pygame.init()  # 1. Initialize Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 2. Create a window
        pygame.display.set_caption("Space Shooter")
        pygame.display.set_icon(pygame.image.load("assets/ufo.png"))
        self.background = self._load_background("bg.png")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()  # 3. Create sprite groups
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = Player()  # 4. Instantiate the player
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            # Limit the frame rate to FPS
            self.clock.tick(FPS)

            self._handle_events()  # Input
            self._update()  # Calculation
            self._draw()  # Rendering

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = self.player.shoot()
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)

    def _update(self):
        self.all_sprites.update()
        if len(self.enemies) < 5:
            if random.randint(1, 60) == 1:
                enemy = Enemy()
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
        # Collision Detection Logic...
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, dokilla=True, dokillb=True)
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.running = False
            print("GAME OVER")

    def _draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # If the background image fails to load, fill with black.
            self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def _load_background(self, name):
        """ Supporting method: Load background image and scale to screen size """
        path = os.path.join("assets", name)
        try:
            image = pygame.image.load(
                path).convert()  # Background images do not require transparency; simply use convert().
            # Scale the background image to fully cover the screen.
            return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print(f"Error: Background image not found in {path}, A solid black background will be used.")
            return None  # If no image is found, return None.
