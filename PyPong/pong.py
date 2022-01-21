from game_objects import *

pg.init()

display = pg.display.set_mode((display_width, display_height))

pg.display.set_caption('PyPong')
title_font = pg.font.SysFont('Cambria', 85, italic=True)

clock = pg.time.Clock()

tick = 0
while True:
    # Обработка событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pause_button.clicked(pg.mouse.get_pos())

    player_racket.move()
    ball.move()
    # Отрисовка обхектов
    display.fill(BACKGROUND)

    for obstacle in obstacles:
        obstacle.draw(display)

    player_racket.draw(display)
    display.blit(title_font.render('PyPong', True, "#28cdcc"), (50, 20))
    ball.draw(display)

    if paused:
        display.blit()
    pause_button.draw_object(display)

    pg.display.update()
    clock.tick(60)

    tick += 1
