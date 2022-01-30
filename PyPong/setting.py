from math import sin, cos, pi

import os
import pygame

pygame.init()

display_width = 1080
display_height = 720
paused = False

score = [0, 0]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = '#190781'

#fonts
title_font = pygame.font.SysFont('Cambria', 85, italic=True)


images_dict = {}
# получаем доступные изображения
for path, dir, file in os.walk(r'./pypong_images'):
    for name_file in file:
        images_dict[name_file] = pygame.image.load(path + '/' + name_file)

blur_surf = pygame.Surface((display_width, display_height))
blur_surf.set_alpha(255)

menu_surf = pygame.Surface((display_width // 3, display_height // 3))


def get_surf_center(surf: pygame.Surface) -> tuple:
    rect = surf.get_rect()
    return (rect.topleft[0] + rect.width // 2, rect.topleft[1] + rect.height // 2)