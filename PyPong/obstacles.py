import pygame as pg

from setting import *


class Border:

    def __init__(self, x, y, width, height, color=BLACK, filled=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pg.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))
        self.color = color
        self.filled = filled

    def draw(self, sc: pg.Surface):
        pygame.draw.rect(self.surf, self.color, self.surf.get_rect(),
                         width=(0 if self.filled is None else self.filled))
        sc.blit(self.surf, (self.x, self.y))


