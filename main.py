import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

from states.menu_state import MenuState
from states.play_state import PlayState
from states.gameover_state import GameOverState
from states.pause_state import PauseState


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Starship Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.states = {
            "menu": MenuState(self),
            "play": PlayState(self),
            "gameover": GameOverState(self),
            "pause": PauseState(self)
        }
        
        self.state_stack = [self.states["menu"]]  # start on menu

        # self.state = self.states["menu"]

    def current_state(self):
        return self.state_stack[-1]
    

    def push_state(self, name, **kwargs):
        state = self.states[name]
        self.state_stack.append(state)
        state.on_enter(**kwargs)

    def pop_state(self):
        # Don't pop the last state
        if len(self.state_stack) > 1:
            top = self.state_stack.pop()
            top.on_exit()

    def change_state(self, name, **kwargs):
        # Replace top state
        self.state_stack[-1].on_exit()
        self.state_stack[-1] = self.states[name]
        self.state_stack[-1].on_enter(**kwargs)

    def peek_under_state(self):
        # Used by PauseState to draw the game behind it
        if len(self.state_stack) >= 2:
            return self.state_stack[-2]
        return self.state_stack[-1]

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                self.current_state().handle_event(event)

            self.current_state().update(dt)
            self.current_state().draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    App().run()
