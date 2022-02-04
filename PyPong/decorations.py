import pygame

import setting

class Decor(pygame.sprite.Sprite):

    def __init__(self, init_x, init_y, speed, group: pygame.sprite.Group):
        super.__init__(self)
        self.x = init_x
        self.y = init_y

        self.target_x = init_x
        self.target_y = init_y

        self.speed = speed

        self.add(group)

    def move(self, ):
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

class decor_label(Decor):

    def __init__(self, init_x: int, init_y: int, width: int, height: int, speed: int,
                 label: pygame.Surface, group: pygame.sprite.Group,
                 background: str = None,border: tuple = None):
        super().__init__(init_x, init_y, speed, group)
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.surf.set_colorkey(setting.BLACK)
        self.x = init_x
        self.y = init_y
        self.speed = speed
        self.label = label
        self.background = background
        self.border = border
        self.target_x = init_x
        self.target_y = init_y

        self.add(group)

    def draw_object(self, sc: pygame.Surface):

        self.surf.fill(self.background if self.background else setting.BLACK)
        if self.border:
            pygame.draw.rect(sc, self.border[1], (self.x, self.y, self.surf.get_width(),
                                                  self.surf.get_height()), width=self.border[0])

        self.surf.blit(self.label, (0, 0))
        sc.blit(self.surf, (self.x, self.y))




class menu(Decor):

    def __init__(self, init_x: int, init_y: int, width: int, height: int, speed: int, button_list: list[tuple], group,
                 background: str = None, border: tuple = None):
        super().__init__(init_x, init_y, speed, group)
        self.init_x = init_x
        self.init_y = init_y
        self.surf = pygame.Surface((width, height))
        self.button_list = button_list
        self.background = background
        self.border = border
        self.speed = speed
        self.target_x = init_x
        self.target_y = init_y

        self.add(group)

