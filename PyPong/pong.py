from game_objects import *

pg.init()

display = pg.display.set_mode((display_width, display_height))

pg.display.set_caption('PyPong')

clock = pg.time.Clock()

tick = 0
while True:
    # Обработка событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pause_button.clicked(pg.mouse.get_pos(), blur_surf, menu_group)

    if not setting.paused:
        player_racket.move()
        ball.move()
        enemy_racket.play(ball)

    # Отрисовка обхектов
    display.blit(BACKGROUND, (17, 28))

    for obstacle in obstacles:
        obstacle.draw(display)

    pause_button.draw_object(display)

    player_score.blit(display)
    enemy_score.blit(display)

    player_racket.draw(display)
    enemy_racket.draw(display)

    # display.blit(title_font.render('PyPong', True, "#28cdcc"), (450, 20))
    ball.draw(display)

    if setting.paused:
        display.blit(blur_surf, (0, 0))
        menu_group.draw(display)

    menu_group.update()
    pg.display.update()
    # if left_border.x + left_border.width + 50 > ball.x and (270 >= ball.angle >= 90):
    #     clock.tick(max((left_border.x + left_border.width + 60 - ball.x) // 2, 3)) # slow-motiom
    clock.tick(60)

    tick += 1

    if not tick % 300:
        enemy_racket.change_mode()
