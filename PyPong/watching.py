import pygame
import pygame as pg
from random import randint
from math import asin, acos, sin, pi, sqrt

pg.init()

display_width, display_height = 800, 600
display = pg.display.set_mode((display_width, display_height))

points_coords = pygame.USEREVENT + 2
pygame.time.set_timer(points_coords, 2000)


class Math:

    @staticmethod
    def from_rads_to_deg(r):
        return r * 180 / pi

    @staticmethod
    def dec_dist(x1, y1, x2, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def calc_angle(abc, ord, rad, quarter):

        if quarter is None:
            return 1, 0, 0, 0
        if quarter % 2:
            ord /= rad
            meas = Math.from_rads_to_deg(asin(min(1., ord)))
        else:
            abc /= rad
            meas = 90 - Math.from_rads_to_deg(acos(min(1., abc)))

        angle = meas + (point.quarter - 1) * 90

        return abc, ord, meas, angle


class Point:

    def __init__(self, x, y, radius, color, speed=3):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.quarter = None

    def draw(self, sc: pg.Surface):
        pg.draw.circle(sc, self.color, (self.x, self.y), self.radius)

    def move(self, rads: int, center: tuple):
        keys = pg.key.get_pressed()
        # if keys[pg.K_UP]:
        #     self.y -= self.speed
        # if keys[pg.K_DOWN]:
        #     self.y += self.speed
        # if keys[pg.K_LEFT]:
        #     self.x -= self.speed
        # if keys[pg.K_RIGHT]:
        #     self.x += self.speed
        if keys[pg.K_DOWN]:
            if self.x >= center[0] and self.y >= center[1]:
                self.quarter = 4
            if self.x <= center[0] and self.y >= center[1]:
                self.quarter = 3
            if self.x <= center[0] and self.y <= center[1]:
                self.quarter = 2
            if self.x >= center[0] and self.y <= center[1]:
                self.quarter = 1
            sec_cat = rads ** 2 - (self.y - center[1]) ** 2
            if self.quarter in [1, 4]:
                self.y += self.speed
                self.x = round(center[0] + sqrt(abs(sec_cat)))
            else:
                self.y -= self.speed
                self.x = round(center[0] - sqrt(abs(sec_cat)))




        elif keys[pg.K_UP]:
            if self.x >= center[0] and self.y <= center[1]:
                self.quarter = 1
            if self.x <= center[0] and self.y <= center[1]:
                self.quarter = 2
            if self.x <= center[0] and self.y >= center[1]:
                self.quarter = 3
            if self.x >= center[0] and self.y >= center[1]:
                self.quarter = 4

            sec_cat = rads ** 2 - (self.y - center[1]) ** 2
            if self.quarter in [1, 4]:
                self.y -= self.speed
                self.x = round(center[0] + sqrt(abs(sec_cat)))
            else:
                self.y += self.speed
                self.x = round(center[0] - sqrt(abs(sec_cat)))
        return # add return


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
        self.os = Point(self.get_surf_center()[0] + width // 2, self.get_surf_center()[1], 10, '#101010', 0)

    def draw(self, sc: pg.Surface, coords: tuple):
        # self.image = pg.transform.rotate(self.image, self.angle)
        self.surf.fill((240, 240, 240))
        self.surf.blit(self.rotated_image, (0, 0))
        pg.draw.rect(self.surf, '#000000', self.rotated_image.get_rect(), width=3)
        sc.blit(self.surf, (self.x, self.y))
        self.os.draw(sc)
        p_x, p_y = coords
        c_x, c_y = self.get_surf_center()
        os_x, os_y = self.os.x, self.os.y
        pg.draw.line(sc, '#FF0000', (p_x, p_y), (os_x, os_y), 3)
        pg.draw.line(sc, '#00FF00', (c_x, c_y), (os_x, os_y), 3)
        pg.draw.line(sc, '#0000FF', (c_x, c_y), (p_x, p_y), 3)
        pg.draw.line(sc, '#00FFFF', (p_x, c_y), (p_x, p_y), 3)
        pg.draw.line(sc, '#FFFF00', (p_x, os_y), (os_x, os_y), 3)

        return (abs(p_x - c_x), abs(p_y - c_y))

    def get_surf_center(self) -> tuple[int, int]:
        return self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2

    # def tg(self, point_coords: tuple):
    #     p_x, p_y = point_coords
    #     c_x, c_y = self.get_surf_center()
    #     prot = p_y - c_y
    #     pril = p_x - c_x
    #     self.angle = atan(prot / pril) * 180 / pi
    #     return prot / pril, self.angle


hank = pg.transform.flip(pg.transform.scale(pg.image.load('./pypong_images/shank.jpg'),
                                            (225, 235)), True, False)
hank_image = image(hank.get_width() * 2, hank.get_height() * 2, display_width // 3, display_height // 4, hank)
rad = hank_image.width // 2
img_center = hank_image.get_surf_center()

point = Point(hank_image.get_surf_center()[0] + hank_image.width // 2,
              hank_image.get_surf_center()[1], 8, '#c2200c', speed=1)

clock = pg.time.Clock()

tick = 0
angle = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        elif event.type == points_coords:
            print(point.quarter, point.x - img_center[0], point.y - img_center[1], rad, rad ** 2 - (point.y - img_center[1]) ** 2)

    display.fill((240, 240, 240))


    ord, abc, meas, angle = Math.calc_angle(*hank_image.draw(display, (point.x, point.y)),
                                  rad, point.quarter)

    point.draw(display)
    pg.draw.circle(display, "#BB0000", hank_image.get_surf_center(), 3)

    pygame.draw.circle(display, '#000000', hank_image.get_surf_center(),
                       hank_image.width // 2, width=2)

    point.move(rad, img_center)

    pg.display.update()

    clock.tick(60)
    tick += 1
    hank_image.rotated_image = pg.transform.rotate(hank_image.image, angle)

    if not tick % 120:
        print(abc, ord, meas, angle)

