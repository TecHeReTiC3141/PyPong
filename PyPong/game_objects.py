from random import *

import pygame.sprite

from buttons import *
from obstacles import *
from decorations import *


class Racket:

    def __init__(self, x: int, y: int, width: int, height: int, direction: str, cool_down=0, speed: int=4, ):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.surf = pg.Surface((self.width, self.height))
        self.surf.set_colorkey(WHITE)
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))
        self.cool_down = cool_down
        self.direction = direction



    def draw(self, sc: pg.Surface):
        self.surf.fill(WHITE)
        pygame.draw.rect(self.surf, '#0000BB', (self.width // 4, 0, self.width // 4 * 3, self.height // 5))
        pygame.draw.rect(self.surf, '#0000BB', (self.width // 4, self.height // 5 * 4, self.width * 3 // 4, self.height // 5))
        pygame.draw.rect(self.surf, '#0000BB', (self.width // 3 * 2, 0, self.width // 3, self.height))
        sc.blit(self.surf, (self.x, self.y))


    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and not self.rect.colliderect(upper_border.rect):
            self.y -= self.speed
        if keys[pg.K_DOWN] and not self.rect.colliderect(lower_border.rect):
            self.y += self.speed
        if keys[pg.K_LEFT] and not self.rect.colliderect(left_border.rect):
            self.x -= self.speed
        if keys[pg.K_RIGHT] and not self.rect.colliderect(mid_border.rect):
            self.x += self.speed
        self.rect.update(self.x, self.y, self.width, self.height)


class TennisBall:

    def __init__(self, x, y, radius, speed, angle=220, cool_down=0, mode=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = angle
        self.rect = pg.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.cool_down = cool_down
        self.speed = speed
        self.mode = mode

    def draw(self, surf):
        pygame.draw.circle(surf, '#a9a016', (self.x, self.y), self.radius)
        pygame.draw.rect(surf, '#AA0000',
                         (self.x + (cos(self.angle / 180 * pi) * self.radius),
                          self.y - (sin(self.angle / 180 * pi)) * self.radius, 10, 10))

    def move(self):
        x_diff = cos(self.angle / 180 * pi) * self.speed
        y_diff = sin(self.angle / 180 * pi) * self.speed

        self.x += round(x_diff)
        self.y -= round(y_diff)
        self.rect.center = (self.x, self.y)
        self.collide()
        self.collide_with_rackets(player_racket)
        self.collide_with_rackets(enemy_racket)
        if y_diff >= 0:
            self.speed *= .999
        else:
            self.speed *= 1.001

        self.cool_down -= 1

    def collide(self):
        if self.rect.colliderect(upper_border.rect):
            self.angle += 2 * (180 - self.angle)

        elif self.rect.colliderect(lower_border.rect):
            self.angle -= 2 * (self.angle - 180)

        elif self.rect.colliderect(left_border.rect):
            score[1] += 1
            enemy_score.update_label(f'{score[1]}')
            if self.angle < 180:
                self.angle -= 2 * (self.angle - 90)
            else:
                self.angle += 2 * (270 - self.angle)

        elif self.rect.colliderect(right_border.rect):
            score[0] += 1
            player_score.update_label(f'{score[0]}')
            if self.angle < 90:
                self.angle += 2 * (90 - self.angle)
            else:
                self.angle -= 2 * (self.angle - 270)

    def collide_with_rackets(self, racket: Racket):
        if self.rect.colliderect(racket.rect) and self.cool_down <= 0:
            self.cool_down = 45
            if self.rect.x >= racket.rect.x + racket.rect.width - 10 and not isinstance(racket, EnemyRacket):
                if self.angle < 180:
                    self.angle -= 2 * (self.angle - 90)
                else:
                    self.angle += 2 * (270 - self.angle)

            elif self.rect.x + self.rect.width <= racket.rect.x + 10 and racket.direction != 'right':
                if self.angle < 90:
                    self.angle += 2 * (90 - self.angle)
                else:
                    self.angle -= 2 * (self.angle - 270)

            elif self.rect.y + self.rect.height <= racket.rect.y + 10:
                self.angle -= 2 * (self.angle - 180)

            elif self.rect.y >= racket.rect.y + racket.rect.height - 10:
                self.angle += 2 * (180 - self.angle)

    def __str__(self):
        return f'{self.x}, {self.y}, {self.rect}'


class EnemyRacket(Racket):

    def __init__(self, x: int, y: int, width: int, height: int, direction: str, cool_down=0, speed: int=4):
        super().__init__(x, y, width, height, cool_down,  direction, speed)
        self.search_rect = pg.Rect(x - width, y - height // 2, width * 3, height * 2)
        self.reverse = 1

    def draw(self, sc: pg.Surface):
        self.surf.fill(WHITE)
        pygame.draw.rect(self.surf, '#BB0000', (0, 0, self.width, self.height // 5))
        pygame.draw.rect(self.surf, '#BB0000', (0, self.height // 5 * 4, self.width, self.height // 5))
        pygame.draw.rect(self.surf, '#BB0000', (0, 0, self.width // 3, self.height))
        sc.blit(self.surf, (self.x, self.y))

    def play(self, ball: TennisBall):
        x, y = ball.x, ball.y
        if y > self.rect.y + self.rect.height * .67:
            if self.reverse > 0 and not self.rect.colliderect(lower_border.rect):
                self.y += self.speed * self.reverse
                self.rect = self.rect.move(0, self.speed * self.reverse)
            elif self.reverse < 0 and not self.rect.colliderect(upper_border.rect):
                self.y += self.speed * self.reverse
                self.rect = self.rect.move(0, self.speed * self.reverse)

        elif y < self.rect.y + self.rect.height * .33:
            if self.reverse > 0 and not self.rect.colliderect(upper_border.rect):
                self.y -= self.speed * self.reverse
                self.rect = self.rect.move(0, -self.speed * self.reverse)
            elif self.reverse < 0 and not self.rect.colliderect(lower_border.rect):
                self.y -= self.speed * self.reverse
                self.rect = self.rect.move(0, -self.speed * self.reverse)

    def change_mode(self):
        mode = randint(1, 100)
        if mode < 80:
            self.speed = 4
            self.reverse = 1
        elif 80 <= mode <= 88:
            self.reverse = -1
        else:
            self.speed = 2


# obstacles
upper_border = Border(0, 0, display_width, display_height // 7, color='#8c9191')
lower_border = Border(0, display_height // 20 * 19, display_width, display_height // 15, color='#8c9191')
left_border = Border(0, 0, display_width // 25, display_height, color='#8c9191')
right_border = Border(display_width // 25 * 24, 0, display_width // 25 + 15, display_height, color='#8c9191')
mid_border = Border(display_width // 2,
                    display_height // 5, display_width // 60, display_height // 3 * 2, color='#f83c08', filled=5)
obstacles = [upper_border, lower_border, mid_border, left_border, right_border]

player_racket = Racket(x=display_width // 4, y=display_height // 2,
                       width=display_width // 30, height=display_height // 8, direction='right')  # Ракетка игрока

enemy_racket = EnemyRacket(x=display_width * 3 // 4, y=display_height // 2,
                       width=display_width // 30, height=display_height // 8, direction='left')

ball = TennisBall(mid_border.x + mid_border.width // 2,
                  randint(mid_border.y, mid_border.y + mid_border.height), display_width // 36, 6)

# buttons
pause_button = Button(display_width // 5 * 4, display_height // 60, display_width // 18, display_height // 12,
                      'pause', border=(BLACK, 10), icon=images_dict['pause_icon.png'])


# surfaces and decorations
menu_group = pygame.sprite.Group()

menu_title = decor_label(display_width // 4, -display_height // 5, display_width // 4, display_height // 5, 3,
                         font=title_font, text='PyPong', color="#19763D", group=menu_group, background=None)

pause_menu = menu(display_width // 3, -display_height // 3, display_width // 3, display_height // 3, 3, [], menu_group)

player_score = decor_label(display_width // 36, display_height // 24, display_width // 36, display_height // 24, 0,
                           font=normal_font, text='0', color='#282828', group=[], background=WHITE, border=(5, BLACK))

enemy_score = decor_label(display_width // 18 * 17, display_height // 24, display_width // 36, display_height // 24, 0,
                           font=normal_font, text='0', color='#282828', group=[], background=WHITE, border=(5, BLACK))

