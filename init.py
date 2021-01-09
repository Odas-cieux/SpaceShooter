from classes import *

# Creation of the screen
screen = pg.display.set_mode(size)

# Creation of the clock
clock = pg.time.Clock()

# Parameters of the mouse
#pg.mouse.set_visible(False)

# Creation of the user's spaceship
image = pg.image.load("ship_1_80_80.png")
rect = image.get_rect()
rect[0] = 210
rect[1] = 520
user_ship = UserShip("User Spaceship", image, 100, rect, cyan, Missile, 15)

# Creation of the list of ennemies
ennemies = []

# Creation of the list of projectiles
projectiles = []
