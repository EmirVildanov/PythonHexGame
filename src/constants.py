from math import *

SIDE = 20
FIELD_SIDE = 11
FIELD_SIZE = FIELD_SIDE ** 2
H1 = SIDE * sin(pi / 3)  # distance between point to main diagonal of hexagon
H2 = SIDE * cos(pi / 3)  # distance between point to H1

APP_NAME = 'He-he-hex'
APP_FONT = 'Comic Sans MS'
SCREEN_WIDTH = int(FIELD_SIDE * 2 * H1 + H1 * (FIELD_SIDE - 1))
SCREEN_HEIGHT = int(2 * SIDE + (FIELD_SIDE - 1) * (2 * SIDE - H2))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
