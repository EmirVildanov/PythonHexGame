from constants import *


def define_hexagon_neighbours_indices(i_index: int, j_index: int):
    """
    Функция, которая определяет индексы соседей
    Клетки с указанными координатами
    """
    hexagon_neighbours_indices = []
    # diagonal left to right
    if i_index - 1 >= 0:
        hexagon_neighbours_indices.append(
            (i_index - 1) * FIELD_SIDE + j_index)
    if i_index + 1 < FIELD_SIDE:
        hexagon_neighbours_indices.append(
            (i_index + 1) * FIELD_SIDE + j_index)
    # diagonal right to left
    if i_index - 1 >= 0 and j_index + 1 < FIELD_SIDE:
        hexagon_neighbours_indices.append(
            (i_index - 1) * FIELD_SIDE + (j_index + 1))
    if i_index + 1 < FIELD_SIDE and j_index - 1 >= 0:
        hexagon_neighbours_indices.append(
            (i_index + 1) * FIELD_SIDE + (j_index - 1))
    # vertical neighbours
    if j_index - 1 >= 0:
        hexagon_neighbours_indices.append(
            i_index * FIELD_SIDE + (j_index - 1))
    if j_index + 1 < FIELD_SIDE:
        hexagon_neighbours_indices.append(
            i_index * FIELD_SIDE + (j_index + 1))
    return hexagon_neighbours_indices


def get_hexagon_coordinates(upper_x: int, upper_y: int, hexagon_side: int):
    """
    Функция, которая возвращает координаты точек шестиугольника
    """
    coordinates = [(upper_x, upper_y)]
    upper_x -= H1
    upper_y += H2
    coordinates.append((upper_x, upper_y))
    upper_y += hexagon_side
    coordinates.append((upper_x, upper_y))
    upper_x += H1
    upper_y += H2
    coordinates.append((upper_x, upper_y))
    upper_x += H1
    upper_y -= H2
    coordinates.append((upper_x, upper_y))
    upper_y -= hexagon_side
    coordinates.append((upper_x, upper_y))
    return coordinates


def find_border_indices(i_index: int, j_index: int):
    """
    Функция, которая определяет рядом с каким из краеё поля находится клетка
    0 - левый
    1 - верхний
    2 - правый
    3 - нижний
    """
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


class Tile:
    """
    Класс, который представляет из себя сущность клетки поля
    """
    def __init__(self, i, j):
        hexagon_index = i * FIELD_SIDE + j
        first_hexagon_upper_x = H1
        first_hexagon_upper_y = 0
        border_indices = find_border_indices(i, j)
        neighbours_indices = define_hexagon_neighbours_indices(i, j)

        upper_x_coordinate = first_hexagon_upper_x + (i * H1) + (j * H1 * 2)
        upper_y_coordinate = first_hexagon_upper_y + (
                i * HEXAGON_SIDE_IN_PX * 3 / 2.)
        coordinates = get_hexagon_coordinates(upper_x_coordinate,
                                              upper_y_coordinate,
                                              HEXAGON_SIDE_IN_PX)
        self.color = WHITE
        self.index = hexagon_index
        self.coordinates = coordinates
        self.neighbours_indices = neighbours_indices
        self.border_indices = border_indices

    def set_color(self, color):
        """
        Функция, которая меняет цвет клетки на указанный
        """
        self.color = color

    def is_empty(self) -> bool:
        """
        Функция, которая проверяет, свободна ли клетка
        """
        return self.color == WHITE
