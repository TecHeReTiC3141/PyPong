import pygame as pg
import pygame.sprite

import setting
from decorations import *


class Button:

    def __init__(self, x, y, width, height, action:str, border:tuple = None, icon: pg.Surface  = None):
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border # border(color, width)
        self.icon = pg.transform.scale(icon, (width, height))
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
            pygame.draw.rect(sc, self.border[0], (self.x, self.y,
                                  self.width, self.height),
                             width=self.border[1])
        self.surf.fill(setting.WHITE)
        if self.icon:
            self.surf.blit(self.icon, (0, 0))
        sc.blit(self.surf, (self.x, self.y))
        self.onfocus()

    def clicked(self, mouse_pos: tuple, *args):
        if self.rect.collidepoint(mouse_pos):
            if self.action == 'pause':
                self.pause(*args)
            elif self.action == 'unpause':
                self.unpause(*args)


    def pause(self, blur_surf: pg.Surface, group: pygame.sprite.Group):
        self.icon = pg.transform.scale(setting.images_dict['play_icon.jpg'],
                                                 (self.width, self.height))
        self.action = 'unpause'
        blur_surf.set_alpha(100)
        for sp in group:
            sp.move_to(setting.display_width // 3, setting.display_height // 3)
        group.update()
        setting.paused = True

    def unpause(self, blur_surf: pg.Surface, group: pygame.sprite.Group):
        self.icon = pg.transform.scale(setting.images_dict['pause_icon.png'],
                                                 (self.width, self.height))
        self.action = 'pause'
        blur_surf.set_alpha(0)
        blur_surf.fill(setting.BLACK)
        for sp in group:
            sp.move_to(setting.display_width // 4, -300)

        group.update()
        setting.paused = False
