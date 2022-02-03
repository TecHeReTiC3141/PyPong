import pygame

from setting import *


class decor_label:

    def __init__(self, init_x: int, init_y: int, width: int, height: int, speed: int,
                 label: str, color: (str, tuple),
                 font: (pygame.font.Font, pygame.font.SysFont) = pygame.font.Font(None, 50),
                 background: str = None,border: tuple = None):
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.surf.set_colorkey(BLACK)
        self.x = init_x
        self.y = init_y
        self.speed = speed
        self.label = label
        self.font = font
        self.color = color
        self.background = background
        self.border = border
        self.target_x = init_x
        self.target_y = init_y

    def draw_object(self, sc: pygame.Surface):

        self.surf.fill(self.background if self.background else BLACK)
        if self.border:
            pygame.draw.rect(sc, self.border[1], (self.x, self.y, self.surf.get_width(),
                                                  self.surf.get_height()), width=self.border[0])

        self.surf.blit(self.font.render(self.label, True, self.color), (0, 0))
        sc.blit(self.surf, (self.x, self.y))
        if self.target_x > self.x:
            self.x += self.speed
        elif self.target_x < self.x:
            self.y -= self.speed
        if self.target_y > self.y:
            self.y += self.speed
        elif self.target_y < self.y:
            self.y -= self.speed

    def move_to(self, targ_x, targ_y):
        self.target_x, self.target_y = targ_x, targ_y


class menu(pygame.Surface):
    pass
