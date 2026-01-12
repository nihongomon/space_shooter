import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from .base_state import BaseState

class MenuState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.items = ["Start Game", "Quit"]
        self.selected = 0

        self.font_item = pygame.font.SysFont(None, 48)
        self.font_hint = pygame.font.SysFont(None, 28)

        self.menu_bg = pygame.image.load("assets/menu_bg.png").convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.app.quit()

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.app.quit()

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.items)

        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.items)

        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            choice = self.items[self.selected]
            if choice == "Start Game":
                self.app.change_state("play")
            elif choice == "Quit":
                self.app.quit()

    def draw(self, screen):
        screen.blit(self.menu_bg, (0, 0))

        start_y = 260
        spacing = 60

        for i, label in enumerate(self.items):
            is_sel = (i == self.selected)
            color = (255, 215, 0) if is_sel else (220, 220, 220)
            surf = self.font_item.render(label, True, color)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
            screen.blit(surf, rect)

            if is_sel:
                left = self.font_item.render(">", True, color)
                right = self.font_item.render("<", True, color)
                screen.blit(left, (rect.left - 50, rect.top))
                screen.blit(right, (rect.right + 20, rect.top))

        hint = self.font_hint.render("Use ↑ ↓ and Enter. Esc quits.", True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 540)))
