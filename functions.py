from init import *

def spawn_ennemies(ennemies):
    prob = rd.random()
    if prob >= 0.995:
        image = pg.image.load("40_40.png")
        rect = image.get_rect()
        x = rd.randint(0, width-rect[2])
        rect[0] = x
        rect[1] = - rect[3]
        ennemies.append(EnnemyShip("Ennemy", image, 30, rect, red, None, 1, 1))

def spawn_projectiles(user_ship, projectiles):
    user_ship.spawn_projectile(projectiles)

def remove_ennemies(ennemies):
    for e in ennemies:
        if e.rect[1] > height:
            ennemies.remove(e)

def remove_projectiles(projectiles):
    for p in projectiles:
        if p.rect[1] + p.rect[3] < 0:
            projectiles.remove(p)

def process_projectiles_collision(projectiles, ennemies):
    for p in projectiles:
        ind_col_enn = p.collision_ennemies(ennemies)
        ind_col_enn.reverse() # the deletion must be in the good order
        for k in ind_col_enn:
            ennemies[k].hp -= p.damages
            if ennemies[k].hp <= 0:
                ennemies.pop(k)
        if ind_col_enn:
            projectiles.remove(p)

def process_ship_collision(user_ship, ennemies):
    ind_col_enn = user_ship.collision_ennemies(ennemies)
    ind_col_enn.reverse() # the deletion must be in the good order
    for k in ind_col_enn:
        ennemies.pop(k)


def movements(user_ship, ennemies, projectiles):
    user_ship.move()
    for e in ennemies:
        e.move_vertically()
    for p in projectiles:
        p.move_vertically()

def display(screen, user_ship, ennemies, projectiles, pause):
    screen.fill(black)
    pg.draw.line(screen, white, [0,600], [width,600], 1)
    user_ship.display(screen)
    for e in ennemies:
        e.display(screen)
    for p in projectiles:
        p.display(screen)
    if pause:
        myfont = pg.font.SysFont("Arial", 30)
        label = myfont.render("PAUSE", 1, white)
        screen.blit(label, (100, 100))
    pg.display.flip()