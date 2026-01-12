import pygame


class GameOverScreen:
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h

        self.bg = pygame.image.load("assets/gameover_bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))


        self.title_font = pygame.font.SysFont(None, 90)
        self.item_font = pygame.font.SysFont(None, 48)
        self.hint_font = pygame.font.SysFont(None, 28)

        self.items = ["Retry", "Main Menu", "Quit"]
        self.selected = 0

    def reset(self):
        """Call this when you enter the gameover screen (optional)."""
        self.selected = 0

    def handle_event(self, event):
        """
        Returns:
          - "retry" to restart the game
          - "menu" to return to main menu
          - "quit" to exit the whole app
          - None to do nothing
        """
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.items)
            return None

        if event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.items)
            return None

        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            choice = self.items[self.selected]
            if choice == "Retry":
                return "retry"
            if choice == "Main Menu":
                return "menu"
            if choice == "Quit":
                return "quit"

        if event.key == pygame.K_ESCAPE:
            return "menu"

        return None

    def draw(self, screen, lives=0, score=None):
        # Background
        screen.blit(self.bg, (0, 0))

        # Title
        # title = self.title_font.render("GAME OVER", True, (255, 80, 80))
        # screen.blit(title, title.get_rect(center=(self.w // 2, 140)))

        # Optional info line
        info_text = f"Score: 0"

        if score is not None:
            info_text = f"   Score: {score}"
        info = self.item_font.render(info_text, True, (230, 230, 230))
        screen.blit(info, info.get_rect(center=(self.w // 2, 220)))

        # Menu items
        y0 = 320
        gap = 60
        for i, label in enumerate(self.items):
            is_sel = (i == self.selected)
            color = (255, 215, 0) if is_sel else (220, 220, 220)

            surf = self.item_font.render(label, True, color)
            rect = surf.get_rect(center=(self.w // 2, y0 + i * gap))
            screen.blit(surf, rect)

            if is_sel:
                left = self.item_font.render(">", True, color)
                right = self.item_font.render("<", True, color)
                screen.blit(left, (rect.left - 60, rect.top))
                screen.blit(right, (rect.right + 25, rect.top))

        # Hint
        hint = self.hint_font.render("Use ↑ ↓ Enter. Esc = Main Menu", True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(self.w // 2, self.h - 40)))
