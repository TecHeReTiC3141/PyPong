import pygame
import pygame as pg
from random import randint
from math import atan, tan, pi

pg.init()

display_width, display_height = 640, 480
display = pg.display.set_mode((display_width, display_height))

class Point:

    def __init__(self, x, y, radius, color, speed=3):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self, sc: pg.Surface):
        pg.draw.circle(sc, self.color, (self.x, self.y), self.radius)

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.y -= self.speed
        if keys[pg.K_DOWN]:
            self.y += self.speed
        if keys[pg.K_LEFT]:
            self.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.x += self.speed


class image:

    def __init__(self, width, height, x, y, image: pg.Surface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image.convert_alpha()
        self.surf = pg.Surface((width, height))
        self.angle = 0
        self.rotated_image = image.copy()

    def draw(self, sc: pg.Surface, coords: tuple):
        # self.image = pg.transform.rotate(self.image, self.angle)
        self.surf.fill((240, 240, 240))
        self.surf.blit(self.rotated_image, (0, 0))
        pg.draw.rect(self.surf, '#000000', self.rotated_image.get_rect(), width=3)
        sc.blit(self.surf, (self.x, self.y))
        p_x, p_y = coords
        c_x, c_y = self.get_surf_center()
        pg.draw.line(sc, '#FF0000', (p_x, c_y), (p_x, p_y), 3)
        pg.draw.line(sc, '#00FF00', (c_x, c_y), (p_x, p_y), 3)
        pg.draw.line(sc, '#0000FF', (c_x, c_y), (p_x, c_y), 3)

    def get_surf_center(self):
        return self.x + self.surf.get_width() // 2, self.y + self.surf.get_height() // 2

    def tg(self, point_coords: tuple):
        p_x, p_y = point_coords
        c_x, c_y = self.get_surf_center()
        prot = p_y - c_y
        pril = p_x - c_x
        self.angle = atan(prot / pril) * 180 / pi
        return prot / pril, self.angle


point = Point(randint(0, 640), randint(0, 480), 8, '#c2200c')
hank = pg.transform.flip(pg.transform.scale(pg.image.load('./pypong_images/shank.jpg'),
                                            (225, 235)), True, False)

hank_image = image(hank.get_width() * 2, hank.get_height() * 2, display_width // 4, display_height // 5, hank)


clock = pg.time.Clock()

tick = 0
angle = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    display.fill((240, 240, 240))
    hank_image.draw(display, (point.x, point.y))
    point.draw(display)

    pg.draw.circle(display, "#BB0000", hank_image.get_surf_center(), 3)

    point.move()

    pg.display.update()

    clock.tick(60)
    tick += 1
    hank_image.rotated_image = pg.transform.rotate(hank_image.image, angle)
    angle += 1
    if not tick % 60:
        print(hank_image.tg((point.x, point.y)))

