import random
from math import asin, acos, pi, sqrt

import pygame
import pygame as pg

pg.init()

display_width, display_height = 1024, 768
visual = False
start = True
display = pg.display.set_mode((display_width, display_height))

points_coords = pygame.USEREVENT + 2
pygame.time.set_timer(points_coords, 2000)

tutor_font = pygame.font.SysFont('Cambria', 40)
tutor_text = ['Hello there', 'WASD - to move the point', 'V - toggle visualisation',
              'M - toggle mouse mode', 'RightEnter to start']


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

    def __init__(self, x, y, radius, rad, color, speed=3):
        self.x = x
        self.y = y
        self.radius = radius
        self.rad = rad
        self.color = color
        self.speed = speed
        self.quarter = None
        self.clockwise = None

    def draw(self, sc: pg.Surface):
        pg.draw.circle(sc, self.color, (self.x, self.y), self.radius)

    def move(self, center: tuple):
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.y = min(self.y + self.speed, display_height)
        if keys[pg.K_UP]:
            self.y = max(self.y - self.speed, 0)
        if keys[pg.K_LEFT]:
            self.x = max(self.x - self.speed, 0)
        if keys[pg.K_RIGHT]:
            self.x = min(self.x + self.speed, display_width)

        self.rad = Math.dec_dist(self.x, self.y, *center)
        self.speed = max(self.rad // 250, 1)
        if self.clockwise:
            if self.x >= center[0] and self.y >= center[1]:
                self.quarter = 4
                self.clockwise = True
            if self.x <= center[0] and self.y >= center[1]:
                self.quarter = 3
            if self.x <= center[0] and self.y <= center[1]:
                self.quarter = 2
            if self.x >= center[0] and self.y <= center[1]:
                self.quarter = 1
                self.clockwise = False
        else:
            if self.x >= center[0] and self.y <= center[1]:
                self.quarter = 1
                self.clockwise = False
            if self.x <= center[0] and self.y <= center[1]:
                self.quarter = 2
            if self.x <= center[0] and self.y >= center[1]:
                self.quarter = 3
            if self.x >= center[0] and self.y >= center[1]:
                self.quarter = 4
                self.clockwise = True


class MousePoint(Point):

    def move(self, center: tuple):
        self.x, self.y = pygame.mouse.get_pos()

        self.rad = Math.dec_dist(self.x, self.y, *center)
        self.speed = max(self.rad // 250, 1)
        if self.clockwise:
            if self.x >= center[0] and self.y >= center[1]:
                self.quarter = 4
                self.clockwise = True
            if self.x <= center[0] and self.y >= center[1]:
                self.quarter = 3
            if self.x <= center[0] and self.y <= center[1]:
                self.quarter = 2
            if self.x >= center[0] and self.y <= center[1]:
                self.quarter = 1
                self.clockwise = False
        else:
            if self.x >= center[0] and self.y <= center[1]:
                self.quarter = 1
                self.clockwise = False
            if self.x <= center[0] and self.y <= center[1]:
                self.quarter = 2
            if self.x <= center[0] and self.y >= center[1]:
                self.quarter = 3
            if self.x >= center[0] and self.y >= center[1]:
                self.quarter = 4
                self.clockwise = True


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

        p_x, p_y = coords
        c_x, c_y = self.get_surf_center()
        os_x, os_y = self.os.x, self.os.y
        if visual:
            self.os.draw(sc)
            pg.draw.aaline(sc, '#FF0000', (p_x, p_y), (os_x, os_y), 3)
            pg.draw.aaline(sc, '#00FF00', (c_x, c_y), (os_x, os_y), 3)
            pg.draw.aaline(sc, '#0000FF', (c_x, c_y), (p_x, p_y), 3)
            pg.draw.aaline(sc, '#00FFFF', (p_x, c_y), (p_x, p_y), 3)
            pg.draw.aaline(sc, '#FFFF00', (p_x, os_y), (os_x, os_y), 3)

        return abs(p_x - c_x), abs(p_y - c_y)

    def get_surf_center(self) -> tuple[int, int]:
        return self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2


tutorial = pygame.Surface((display_width // 3 * 2, display_height // 3))

hank = pg.transform.flip(pg.transform.scale(pg.image.load('./pypong_images/shank.png'),
                                            (225, 235)), True, False)
hank_image = image(hank.get_width() * 2, hank.get_height() * 2, display_width // 3, display_height // 4, hank)

img_center = hank_image.get_surf_center()

point = Point(x := random.randint(0, display_width), y := random.randint(0, display_height),
              8, Math.dec_dist(x, y, *hank_image.get_surf_center()), '#c2200c', speed=1)

mouse_point = Point(*pygame.mouse.get_pos(),
                    8, Math.dec_dist(x, y, *hank_image.get_surf_center()), '#c2200c', speed=1)

clock = pg.time.Clock()

tick = 0
angle = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        elif visual and event.type == points_coords:
            print(point.quarter, point.x - img_center[0], point.y - img_center[1], point.rad)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                visual = ~visual
            elif event.key == pygame.K_KP_ENTER:
                start = False

    display.fill((240, 240, 240))

    ordin, abc, meas, angle = Math.calc_angle(*hank_image.draw(display, (point.x, point.y)),
                                              point.rad, point.quarter)
    point.draw(display)
    if visual and not start:
        pg.draw.circle(display, "#BB0000", hank_image.get_surf_center(), 3)

        pygame.draw.circle(display, '#000000', hank_image.get_surf_center(),
                           point.rad, width=2)
    if not start:
        point.move(img_center)

    if start:
        tutorial.fill('#BBBBBB')
        for i in range(len(tutor_text)):
            tutorial.blit(tutor_font.render(tutor_text[i], True, (0, 0, 0)),
                          (tutorial.get_width() // 2 - len(tutor_text[i]) * 8, 20 + i * 40))
            pygame.draw.rect(display, '#000000', display.blit(tutorial, (0, display_height // 3 * 2)), width=5)

    pg.display.update()

    clock.tick(60)
    tick += 1
    hank_image.rotated_image = pg.transform.rotate(hank_image.image, angle)

    if not tick % 120:
        print(abc, ordin, meas, angle)
