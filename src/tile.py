from constants import *


def define_hexagon_neighbours_indices(i_index, j_index):
    hexagon_neighbours_indices = []
    # diagonal left to right
    if i_index - 1 >= 0:
        hexagon_neighbours_indices.append((i_index - 1) * FIELD_SIDE + j_index)
    if i_index + 1 < FIELD_SIDE:
        hexagon_neighbours_indices.append((i_index + 1) * FIELD_SIDE + j_index)
    # diagonal right to left
    if i_index - 1 >= 0 and j_index + 1 < FIELD_SIDE:
        hexagon_neighbours_indices.append((i_index - 1) * FIELD_SIDE + (j_index + 1))
    if i_index + 1 < FIELD_SIDE and j_index - 1 >= 0:
        hexagon_neighbours_indices.append((i_index + 1) * FIELD_SIDE + (j_index - 1))
    # vertical neighbours
    if j_index - 1 >= 0:
        hexagon_neighbours_indices.append(i_index * FIELD_SIDE + (j_index - 1))
    if j_index + 1 < FIELD_SIDE:
        hexagon_neighbours_indices.append(i_index * FIELD_SIDE + (j_index + 1))
    return hexagon_neighbours_indices


def get_hexagon_coordinates(upper_x: int, upper_y: int, hexagon_side: int, h1, h2):
    coordinates = [(upper_x, upper_y)]
    upper_x -= h1
    upper_y += h2
    coordinates.append((upper_x, upper_y))
    upper_y += hexagon_side
    coordinates.append((upper_x, upper_y))
    upper_x += h1
    upper_y += h2
    coordinates.append((upper_x, upper_y))
    upper_x += h1
    upper_y -= h2
    coordinates.append((upper_x, upper_y))
    upper_y -= hexagon_side
    coordinates.append((upper_x, upper_y))
    return coordinates


def find_border_indices(i_index, j_index):
    border_indices = []
    if j_index == 0:
        border_indices.append(0)
    elif j_index == FIELD_SIDE - 1:
        border_indices.append(2)
    if i_index == 0:
        border_indices.append(1)
    elif i_index == FIELD_SIDE - 1:
        border_indices.append(3)
    return border_indices


def find_hexagon_cube_coordinates(i: int, j: int):
    # (0, 0) - is a center of cube coordinate system. watch https://www.redblobgames.com/grids/hexagons/
    x = j
    y = -(i + j)
    z = i
    return x, y, z


class Tile:
    def __init__(self, i, j):
        hexagon_index = i * FIELD_SIDE + j
        first_hexagon_upper_x = H1
        first_hexagon_upper_y = 0
        border_indices = find_border_indices(i, j)
        neighbours_indices = define_hexagon_neighbours_indices(i, j)

        upper_x_coordinate = first_hexagon_upper_x + (i * H1) + (j * H1 * 2)
        upper_y_coordinate = first_hexagon_upper_y + (i * HEXAGON_SIDE_IN_PX * 3 / 2.)
        coordinates = get_hexagon_coordinates(upper_x_coordinate, upper_y_coordinate, HEXAGON_SIDE_IN_PX, H1, H2)
        cube_coordinates = find_hexagon_cube_coordinates(i, j)
        self.color = WHITE
        self.index = hexagon_index
        self.coordinates = coordinates
        self.cube_coordinates = cube_coordinates
        self.neighbours_indices = neighbours_indices
        self.border_indices = border_indices

    def set_color(self, color):
        if self.color == WHITE:
            self.color = color
        else:
            print("SOMETHING WENT WRONG")

    def is_empty(self) -> bool:
        return self.color == WHITE


def find_hexagon_cube_distance(tile1: Tile, tile2: Tile):
    x_diff = tile1.cube_coordinates[0] - tile2.cube_coordinates[0]
    y_diff = tile1.cube_coordinates[1] - tile2.cube_coordinates[1]
    z_diff = tile1.cube_coordinates[2] - tile2.cube_coordinates[2]
    return (abs(x_diff) + abs(y_diff) + abs(z_diff)) / 2
