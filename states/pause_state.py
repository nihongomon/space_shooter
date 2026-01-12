import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from .base_state import BaseState

class PauseState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.SysFont(None, 96)
        self.hint = pygame.font.SysFont(None, 28)

        # A dim overlay looks nicer than raw text on top
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 140))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.app.quit()

        if event.type == pygame.KEYDOWN:
            # ESC (or Enter) to resume
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.app.pop_state()

    def update(self, dt):
        # Do nothing -> freezes gameplay
        pass

    def draw(self, screen):
        # Draw the state underneath (the game) first
        self.app.peek_under_state().draw(screen)

        # Overlay + PAUSED text
        screen.blit(self.overlay, (0, 0))

        paused = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(paused, paused.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        hint = self.hint.render("Press ESC (or Enter) to resume", True, (220, 220, 220))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))
