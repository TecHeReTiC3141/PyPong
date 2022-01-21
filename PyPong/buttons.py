import pygame as pg
from setting import *

class Button:

    def __init__(self, x, y, width, height, action, border:tuple = None, icon_path: str = None):
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border # border(color, width)

        self.icon = pg.transform.scale(pg.image.load(icon_path), (width, height))
        self.surf = pg.Surface((width, height))
        self.rect = pg.Rect(x, y, width, height)
        self.infocus = False

    def onfocus(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.infocus:
            self.x = self.rect.x - 10
            self.y = self.rect.y - 10
            self.width = self.rect.width + 20
            self.height = self.rect.height + 20
            self.surf = pg.Surface((self.width, self.height))
            self.icon = pg.transform.scale(self.icon, (self.width, self.height))
            self.infocus = True

        elif not self.rect.collidepoint(mouse_pos) and self.infocus:
            self.x = self.rect.x
            self.y = self.rect.y
            self.width = self.rect.width
            self.height = self.rect.height
            self.surf = pg.Surface((self.width, self.height))
            self.icon = pg.transform.scale(self.icon, (self.width, self.height))
            self.infocus = False

    def draw_object(self, sc: pg.Surface):
        if self.border:
            pygame.draw.rect(sc, self.border[0], (self.x - self.border[1], self.y - self.border[1],
                                  self.width + self.border[1] * 2, self.height + self.border[1] * 2),
                             width=self.border[1])
        self.surf.fill(WHITE)
        if self.icon:
            self.surf.blit(self.icon, (0, 0))
        sc.blit(self.surf, (self.x, self.y))
        self.onfocus()

    def clicked(self, mouse_pos: tuple):
        if self.rect.collidepoint(mouse_pos):
            self.action()


def pause(button_trigger: Button, blur_surf: pg.Surface, pause_surf: pg.Surface):
    global paused
    button_trigger.icon = pg.transform.scale(images_dict['play_icon.jpg'],
                                             (button_trigger.width, button_trigger.height))
    button_trigger.action = unpause
    blur_surf.set_alpha(60)
    paused = True

def unpause(button_trigger: Button, blur_surf: pg.Surface, pause_surf: pg.Surface):
    global paused
    button_trigger.icon = pg.transform.scale(images_dict['pause_icon.jpg'],
                                             (button_trigger.width, button_trigger.height))
    button_trigger.action = pause
    blur_surf.set_alpha(255)
    paused = False

