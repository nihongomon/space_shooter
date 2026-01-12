import pygame
import random


def make_star_layer(w, h, count=160):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for _ in range(count):
        x = random.randrange(w)
        y = random.randrange(h)
        r = random.choice([1, 1, 1, 2])
        pygame.draw.circle(surf, (255, 255, 255, 200), (x, y), r)
    return surf


def make_cloud_layer(w, h, blobs, color, alpha):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for _ in range(blobs):
        cx = random.randrange(-100, w + 100)
        cy = random.randrange(h)
        rw = random.randrange(120, 280)
        rh = random.randrange(40, 120)
        for _ in range(4):
            ox = random.randrange(-rw // 3, rw // 3)
            oy = random.randrange(-rh // 3, rh // 3)
            rrw = int(rw * random.uniform(0.6, 1.0))
            rrh = int(rh * random.uniform(0.6, 1.0))
            rect = pygame.Rect(cx + ox, cy + oy, rrw, rrh)
            pygame.draw.ellipse(surf, (*color, alpha), rect)
    return surf


class _VerticalLayer:
    def __init__(self, image: pygame.Surface, speed: float):
        self.image = image
        self.speed = speed
        self.y = 0.0
        self.h = image.get_height()

    def update(self, dt: float):
        self.y += self.speed * dt  # move DOWN
        self.y %= self.h

    def draw(self, target: pygame.Surface):
        y1 = -self.y
        target.blit(self.image, (0, y1))
        target.blit(self.image, (0, y1 + self.h))


class ParallaxBackground:
    """
    Vertical parallax background for an (w,h) screen.
    Call update(dt_seconds) each frame, then draw(screen).
    """
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h

        stars = make_star_layer(w, h, count=160)
        far_fog = make_cloud_layer(w, h, blobs=10, color=(120, 160, 200), alpha=70)
        near_fog = make_cloud_layer(w, h, blobs=14, color=(180, 210, 230), alpha=95)

        self.layers = [
            _VerticalLayer(stars, speed=20),
            _VerticalLayer(far_fog, speed=50),
            _VerticalLayer(near_fog, speed=90),
        ]

    def update(self, dt_seconds: float):
        for layer in self.layers:
            layer.update(dt_seconds)

    def draw(self, screen: pygame.Surface):
        # base sky color
        screen.fill((10, 12, 30))
        for layer in self.layers:
            layer.draw(screen)
