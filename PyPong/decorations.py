import pygame

import setting


class Decor(pygame.sprite.Sprite):

    def __init__(self, init_x, init_y, width, height, speed, group: pygame.sprite.Group):

        super().__init__(group)

        self.x = init_x
        self.y = init_y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(init_x, init_y, width, height)
        self.image.set_colorkey(setting.BLACK)
        self.target_x = init_x
        self.target_y = init_y

        self.speed = speed

    def update(self):
        if self.target_x > self.x:
            self.x += self.speed
            self.rect.move(self.speed, 0)
        elif self.target_x < self.x:
            self.y -= self.speed
            self.rect.move(-self.speed, 0)
        if self.target_y > self.y:
            self.y += self.speed
            self.rect.move(0, self.speed)
        elif self.target_y < self.y:
            self.y -= self.speed
            self.rect.move(0, -self.speed)

    def __repr__(self):
        pass


    def move_to(self, targ_x, targ_y):
        self.target_x, self.target_y = targ_x, targ_y


class decor_label(Decor):

    def __init__(self, init_x: int, init_y: int, width: int, height: int, speed: int,
                 text: str, color: str, font, group: pygame.sprite.Group,
                 background: str = None, border: tuple = None):
        Decor.__init__(self, init_x, init_y, width, height, speed, group)

        self.x = init_x
        self.y = init_y
        self.speed = speed
        self.text = text
        self.font = font
        self.color = color
        self.label = font.render(text, True, color)
        self.background = background
        self.border = border
        self.target_x = init_x
        self.target_y = init_y

        self.add(group)

    def blit(self, sc: pygame.Surface):
        self.image.fill(self.background if self.background else setting.BLACK)
        if self.border:
            pygame.draw.rect(sc, self.border[1], (self.x, self.y, self.image.get_width(),
                                                  self.image.get_height()), width=self.border[0])

        self.image.blit(self.label, (0, 0))
        sc.blit(self.image, (self.x, self.y))

    def update_label(self, new: str):
        self.text = new
        self.label = self.font.render(self.text, True, self.color)


class menu(Decor):

    def __init__(self, init_x: int, init_y: int, width: int, height: int, speed: int, button_list: list[tuple], group,
                 background: str = None, border: tuple = None):
        Decor.__init__(self, init_x, init_y, width, height, speed, group)
        self.init_x = init_x
        self.init_y = init_y
        self.image = pygame.Surface((width, height))
        self.button_list = button_list
        self.background = background
        self.border = border
        self.speed = speed
        self.target_x = init_x
        self.target_y = init_y

        self.add(group)
