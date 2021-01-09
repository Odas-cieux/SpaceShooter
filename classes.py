import pygame as pg
import math
import sys
import random as rd

pg.init()

# Constants
fps = 200
white = 255, 255, 255
black = 0, 0, 0
cyan = 0, 255, 255
red = 255, 0, 0
size = width, height = 500, 700

# Functions

class Ship:

    def __init__(self, name, image, max_hp, rect, color, projectile):
        self.name = name
        self.image = image
        self.hp = max_hp
        self.max_hp = max_hp
        self.rect = rect
        self.color = color
        self.projectile = projectile
        self.counter_period = -1

    def __str__(self):
        #Méthode appelée lors d'une conversion de l'objet en chaîne
        return "Ship : {0}, hp : {1} / {2}, rect : {3}, color : {4}"\
            .format(self.name, self.hp, self.max_hp, self.rect, self.color)

    def display(self, screen):
        screen.blit(self.image, self.rect)
        coins = [(self.rect[0], self.rect[1]), \
                (self.rect[0]+self.rect[2]-1, self.rect[1]), \
                (self.rect[0]+self.rect[2]-1, self.rect[1]+self.rect[3]-1), \
                (self.rect[0], self.rect[1]+self.rect[3]-1)]
        pg.draw.lines(screen, self.color, True, coins)

    def collision(self, ship):
        return self.rect.colliderect(ship.rect)

class UserShip(Ship):

    def __init__(self, name, image, max_hp, rect, color, projectile, inertia):
        self.inertia = inertia
        Ship.__init__(self, name, image, max_hp, rect, color, projectile)

    def move(self):

        # Definitions
        x_mouse, y_mouse = pg.mouse.get_pos()
        x_center = self.rect[0] + self.rect[2] // 2 - 1
        y_center = self.rect[1] + self.rect[3] // 2 - 1
        distance_x = abs(x_mouse - x_center)
        distance_y = abs(y_mouse - y_center)

        # Set the step on x and y
        if x_mouse > x_center:
            step_x = 1 + distance_x // self.inertia
        else:
            step_x = - 1 - distance_x // self.inertia
        if y_mouse > y_center:
            step_y = 1 + distance_y // self.inertia
        else:
            step_y = - 1 - distance_y // self.inertia

        # Stability of the image
        if distance_x <= 1:
            step_x = 0
        if distance_y <= 1:
            step_y = 0

        # Compute a new rect
        self.rect = self.rect.move(step_x,step_y)

        # Restriction on borders
        if self.rect[0] < 0:
            self.rect.move_ip(-self.rect[0], 0)
        elif self.rect[0] > width - self.rect[2]:
            self.rect.move_ip(-self.rect[0] + width - self.rect[2], 0)
        if self.rect[1] < 0:
            self.rect.move_ip(0, -self.rect[1])
        elif self.rect[1] > height - self.rect[3]:
            self.rect.move_ip(0, -self.rect[1] + height - self.rect[3])

    def collision_ennemies(self, ennemies):
        ennemies_rect = get_ennemies_rects(ennemies)
        indices = self.rect.collidelistall(ennemies_rect)
        return indices

    def spawn_projectile(self, projectiles):
        self.counter_period += 1
        if self.counter_period == self.projectile().period:
            self.counter_period = -1
            image = self.projectile().image
            projectile_rect = image.get_rect()
            x_center = self.rect[0] + self.rect[2] // 2 - 1
            projectile_rect[0] = x_center - projectile_rect[2] // 2 + 1
            projectile_rect[1] = self.rect[1]
            projectiles.append(self.projectile().create(projectile_rect))

class EnnemyShip(Ship):
    def __init__(self, name, image, max_hp, rect, color, projectile, slowness, step):
        self.slowness = slowness
        self.counter_slow = -1
        self.step = step
        Ship.__init__(self, name, image, max_hp, rect, color, projectile)

    def move_vertically(self):
        self.counter_slow += 1
        if self.counter_slow == self.slowness:
            self.counter_slow = -1
            self.rect[1] = self.rect[1] + self.step

class Projectile:

    def __init__(self, name, image, slowness, step, damages, period, create):
        self.name = name
        self.image = image
        self.slowness = slowness
        self.counter_slow = -1
        self.step = step
        self.damages = damages
        self.period = period
        self.create = create

    def move_vertically(self):
        self.counter_slow += 1
        if self.counter_slow == self.slowness:
            self.counter_slow = -1
            self.rect[1] = self.rect[1] - self.step

class Projectile_obj():

    def __init__(self, name, image, slowness, step, damages, period, rect):
        self.rect = rect
        Projectile.__init__(self, name, image, slowness, step, damages, period)

    def __str__(self):
        #Méthode appelée lors d'une conversion de l'objet en chaîne
        return "Projectile : {0}, damages : {1}"\
            .format(self.name, self.damages)

    def display(self, screen):
        screen.blit(self.image, self.rect)

    def collision_ennemies(self, ennemies):
        ennemies_rect = get_ennemies_rects(ennemies)
        indices = self.rect.collidelistall(ennemies_rect)
        return indices

class Missile(Projectile):

    def __init__(self):
        name = "Missile"
        image = pg.image.load("missile_6_14.png")
        slowness = 0
        step = 2
        damages = 10
        period = 30
        create = Missile_obj
        Projectile.__init__(self, name, image, slowness, step, damages, period, create)

class Missile_obj(Missile, Projectile_obj):

    def __init__(self, rect):
        self.rect = rect
        Missile.__init__(self)

# Functions
def get_ennemies_rects(ennemies):
    ennemies_rect = []
    for e in ennemies:
        ennemies_rect.append(e.rect)
    return ennemies_rect
    



