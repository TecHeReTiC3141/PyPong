import os

display_width = 1080
display_height = 720


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

images_dict = {}

for path, dir, file in os.walk('pypong_images'):
    print(path, file)
    for name_file in file:
        images_dict[name_file] = os.path.join(path, name_file)
print(images_dict)
