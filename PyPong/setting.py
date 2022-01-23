from math import sin, cos, pi

import os
import pygame

display_width = 1080
display_height = 720
paused = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = '#190781'


images_dict = {}
# получаем доступные изображения
for path, dir, file in os.walk(r'./pypong_images'):
    for name_file in file:
        images_dict[name_file] = pygame.image.load(path + '/' + name_file)

blur_surf = pygame.Surface((display_width, display_height))
blur_surf.set_alpha(255)

menu_surf = pygame.Surface((display_width // 3, display_height // 3))