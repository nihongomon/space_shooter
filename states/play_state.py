import random
import pygame

from config import *
from parallax import ParallaxBackground
from sprites.enemy import Enemy
from sprites.player import Player
from .base_state import BaseState

class PlayState(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.parallax = ParallaxBackground(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ui_font = pygame.font.SysFont(None, 36)

        self.reset_game()

    def on_enter(self, **kwargs):
        # Reset unless you explicitly say "resume"
        if not kwargs.get("resume", False):
            self.reset_game()

    def reset_game(self):
        self.lives = 3
        self.invincible_until = 0
        self.score = 0

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.app.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.push_state("pause")
                return
            
            if event.key == pygame.K_ESCAPE:
                self.app.change_state("menu")

            if event.key == pygame.K_SPACE:
                bullet = self.player.shoot()
                if bullet:
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)

    def update(self, dt):
        self.parallax.update(dt)
        self.all_sprites.update()

        # Spawn enemies
        if len(self.enemies) < 5 and random.randint(1, 60) == 1:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # Bullet vs enemy collisions
        hit_enemy = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if hit_enemy:
            self.score += 10 * len(hit_enemy)

        now = pygame.time.get_ticks()

        # Player hit check
        if now >= self.invincible_until:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if hits:
                self.lives -= 1
                self.invincible_until = now + 1200
                self.player.trigger_hit_flash(1000)

                if self.lives <= 0:
                    # Switch to gameover, pass score
                    self.app.change_state("gameover", score=self.score)

        # Visual effects (red flash / invincible)
        self.player.apply_visual_effects(now < self.invincible_until)

    def draw(self, screen):
        self.parallax.draw(screen)
        self.all_sprites.draw(screen)

        score_surf = self.ui_font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        lives_surf = self.ui_font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_surf, (10, 40))
