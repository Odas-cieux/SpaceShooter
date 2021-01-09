from functions import *

while 1:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    pause = not pg.mouse.get_focused()
    if not pause:

        spawn_ennemies(ennemies)

        spawn_projectiles(user_ship, projectiles)

        movements(user_ship, ennemies, projectiles)

        process_projectiles_collision(projectiles, ennemies)

        process_ship_collision(user_ship, ennemies)

        remove_projectiles(projectiles)

        remove_ennemies(ennemies)

        
    display(screen, user_ship, ennemies, projectiles, pause)

    # Contrains a fps
    clock.tick(fps)
