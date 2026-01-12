import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from screens.game_over import GameOverScreen
from .base_state import BaseState

class GameOverState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.screen_ui = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score = 0

    def on_enter(self, **kwargs):
        self.score = kwargs.get("score", 0)
        self.screen_ui.reset()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.app.quit()

        action = self.screen_ui.handle_event(event)
        if action == "retry":
            # reset play state and go play
            self.app.states["play"].reset_game()
            self.app.change_state("play")
        elif action == "menu":
            self.app.change_state("menu")
        elif action == "quit":
            self.app.quit()

    def draw(self, screen):
        self.screen_ui.draw(screen, score=self.score)
