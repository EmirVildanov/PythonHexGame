from typing import Sequence, List, Tuple
from queue import Queue

from constants import *
from tile import Tile
import random


def visit_neighbours(hexagons: Sequence[Tile], index: int,
                     visit_list: List[bool],
                     color: Tuple[int],
                     borders_list: Sequence[int] = None):
    """
    Функция, которая посещает всех соседей данного цвета и помечает их в
    visit_list. Возвращает visit_list
    """
    if borders_list is None:
        borders_list = []
    current_hexagon = hexagons[index]
    visit_list[index] = True
    borders_list.extend(current_hexagon.border_indices)
    for neighbour_indx in current_hexagon.neighbours_indices:
        if not visit_list[neighbour_indx] \
                and hexagons[neighbour_indx].color == color:
            visit_neighbours(hexagons, neighbour_indx, visit_list,
                             color,
                             borders_list)
    return visit_list


def find_game_winner(hexagons: Sequence[Tile], index: int, color: Tuple[int]):
    """
    Функция, которая проверяет, кто победит, если поставить в клетку с
    указанным индексом указанный цвет. Возвразщает цвет из трёх вариантов:
    WHITE, BLUE, RED
    """
    hexagons_visiting_list = [False for _ in
                              range(
                                  FIELD_SIZE)]
    visited_borders_list = []
    visit_neighbours(hexagons, index, hexagons_visiting_list, color,
                     visited_borders_list)
    game_winner = WHITE
    if color == BLUE and (
            0 in visited_borders_list and 2 in visited_borders_list):
        game_winner = BLUE
    elif color == RED and (
            1 in visited_borders_list and 3 in visited_borders_list):
        game_winner = RED
    return game_winner


class Bot:
    """
    Класс, который представляет из себя сущность бота,
    который будет играть против реального игрока
    """
    def __init__(self, color: Tuple[int]):
        self.color = color


def find_opposite_color(color: Tuple[int]):
    """
    Функция, которая возвращает противоположенный цвет
    """
    if color == RED:
        return BLUE
    return RED


def find_winning_tiles_for_color(hexagons: Sequence[Tile],
                                 empty_tiles: Sequence[Tile],
                                 color: Tuple[int]):
    """
    Функция, которая возвращает победные клетки для указанного цвета
    То есть клетки, после закрашивания которых указанный цвет
    Победит
    """
    player_winning_tiles = []
    for tile in empty_tiles:
        winner_color = find_game_winner(hexagons, tile.index, color)
        if winner_color == color:
            player_winning_tiles.append(tile)
    return player_winning_tiles


def find_neighbour_tiles(hexagons: Sequence[Tile], tiles: Sequence[Tile]):
    """
    Функция, которая возвращает список всех соседних клеток
    из переданного списка
    """
    neighbour_indices = []
    for tile in tiles:
        neighbour_indices = neighbour_indices + list(
            set(tile.neighbours_indices) - set(neighbour_indices))
    return [hexagons[index] for index in neighbour_indices]


def find_concrete_border_tiles(hexagons: Sequence[Tile],
                               border_tiles: Sequence[Tile],
                               color: Tuple[int]):
    """
    Функция, которая возвращает клетки, окружающие определённую границу и
    все закрашенные клетки, которые находятся рядом с границей
    """
    visit: List[bool] = [False for _ in range(FIELD_SIZE)]
    for tile in border_tiles:
        if tile.color == color and visit[tile.index] is False:
            visit = visit_neighbours(hexagons, tile.index, visit, color)
    border_tiles = [tile for tile in border_tiles if
                    tile not in visit]
    border_visiting_list_tiles = [hexagon for hexagon in hexagons if
                                  visit[hexagon.index] is True]
    neighbours = find_neighbour_tiles(hexagons, border_visiting_list_tiles)
    all_border_tiles = border_tiles + list(
        set(neighbours) - set(border_tiles))
    empty_border_tiles = list(
        filter(lambda tile: tile.is_empty(), all_border_tiles))
    return empty_border_tiles


def find_field_border_tiles(hexagons: Sequence[Tile],
                            computer_color: Tuple[int]):
    """
    Функция, которая возвращает два массива клеток, которые
    нужно закрасить, чтобы коснуться границы
    Два массива клеток представляют собой массивы граничных
    клеток двух противоположенных сторон поля
    """
    if computer_color == BLUE:
        border1_tiles = [hexagon for hexagon in hexagons if
                         0 in hexagon.border_indices]
        border2_tiles = [hexagon for hexagon in hexagons if
                         2 in hexagon.border_indices]
    else:
        border1_tiles = [hexagon for hexagon in hexagons if
                         1 in hexagon.border_indices]
        border2_tiles = [hexagon for hexagon in hexagons if
                         3 in hexagon.border_indices]

    border1_tiles = find_concrete_border_tiles(hexagons, border1_tiles,
                                               computer_color)
    border2_tiles = find_concrete_border_tiles(hexagons, border2_tiles,
                                               computer_color)
    return border1_tiles, border2_tiles


def find_all_distances_from_tile(hexagons: Sequence[Tile],
                                 tile: Tile) -> Sequence[int]:
    """
    Функция, которая возвращает массив расстояний
    от данной клетки до всех остальных клеток поля
    Если из данной клетки нет пути в другую клетку,
    расстояние между ними равно -1
    """
    tiles_distances = [-1 for i in range(FIELD_SIZE)]
    frontier = Queue()
    frontier.put((tile, 0))  # tile and distance from tile
    reached = set()
    reached.add(tile)

    while not frontier.empty():
        current_pair = frontier.get()
        for next_tile in find_neighbours_of_not_opposite_color(hexagons,
                                                               current_pair[
                                                                   0],
                                                               tile.color):
            if next_tile not in reached:
                frontier.put((next_tile, current_pair[1] + 1))
                reached.add(next_tile)
                tiles_distances[next_tile.index] = current_pair[1] + 1
    return tiles_distances


def find_neighbours_of_not_opposite_color(hexagons: Sequence[Tile],
                                          tile: Tile, color: Tuple[int]):
    """
    Функция, которая возвращает соседей всех клеток из переданного списка,
    которые либо пусты, либо имеют цвет, переданный как параметр
    """
    neighbours = []
    for neighbour_index in tile.neighbours_indices:
        if hexagons[neighbour_index].color != find_opposite_color(color):
            neighbours.append(hexagons[neighbour_index])
    return neighbours


def find_path_from_tile_to_tile(hexagons: Sequence[Tile], tile1: Tile,
                                tile2: Tile) -> List[Tile]:
    """
    Функция, которая возвращает массив клеток поля,
    представляющий путь из клетки tile1 в клетку tile2
    """
    frontier = Queue()
    frontier.put(tile1)
    came_from = dict()
    came_from[tile1] = None

    while not frontier.empty():
        current = frontier.get()
        for next_tile in find_neighbours_of_not_opposite_color(hexagons,
                                                               current,
                                                               tile1.color):
            if next_tile not in came_from:
                frontier.put(next_tile)
                came_from[next_tile] = current

    current = tile2
    path = []
    while current != tile1:
        path.append(current)
        current = came_from[current]
    path.append(tile1)
    path.reverse()
    return path


def make_easy_computer_turn(hexagons: Sequence[Tile],
                            empty_tiles: Sequence[Tile],
                            computer_color: Tuple[int]):
    """
    Функция, которая вернёт индекс случайной клетки, расположенной
    рядом с одной из закрашенных клеток игрока
    Считается не самым умным ходом бота
    """
    player_colored_tiles = [hexagon for hexagon in hexagons if
                            hexagon.color == find_opposite_color(
                                computer_color)]
    tiles_next_to_player = find_neighbour_tiles(hexagons,
                                                player_colored_tiles)
    return random.choice(
        [tile for tile in empty_tiles if tile in tiles_next_to_player])


def make_hard_computer_turn(hexagons: Sequence[Tile],
                            computer_color: Tuple[int]):
    """
    Функция, которая вернёт индекс клетки, которая
    начнёт строить цепь от одной границы поля, выигрышной для бота
    до другой
    """
    border1_tiles, border2_tiles = find_field_border_tiles(hexagons,
                                                           computer_color)
    board_distances_pairs = []  # distances from board1 to board2
    for tile1 in border1_tiles:
        distance_from_tile1_to_all_tiles = find_all_distances_from_tile(
            hexagons, tile1)
        for tile2 in border2_tiles:
            distance_from_tile1_to_tile2 = distance_from_tile1_to_all_tiles[
                tile2.index]
            if distance_from_tile1_to_tile2 != -1:
                board_distances_pairs.append(
                    (tile1, tile2, distance_from_tile1_to_tile2))
    board_distances_pairs = sorted(
        board_distances_pairs,
        key=lambda element: element[2])
    best_distances_pairs = list(
        filter(lambda element: element[2] == board_distances_pairs[0][2],
               board_distances_pairs))
    best_pair = random.choice(best_distances_pairs)

    computer_path = find_path_from_tile_to_tile(hexagons, best_pair[0],
                                                best_pair[1])
    return [tile for tile in computer_path if tile.is_empty()][0]


def find_best_tile_for_bot(hexagons: Sequence[Tile],
                           computer_color: Tuple[int]):
    """
    Функция, которая вернёт наиболее подходящий индекс клетки
    для компьютера в следующем приоритете:
    1) Победная для компьютера клетка
    2) Победная для игрока клетка
    3.1) Либо клетка "простого" хода
    3.2) Либо клетка "сложного" хода
    """
    empty_tiles = [hexagon for hexagon in hexagons if hexagon.color == WHITE]
    player_winning_tiles = find_winning_tiles_for_color(hexagons, empty_tiles,
                                                        find_opposite_color(
                                                            computer_color))
    computer_winning_tiles = find_winning_tiles_for_color(hexagons,
                                                          empty_tiles,
                                                          computer_color)
    if len(computer_winning_tiles) != 0:
        return random.choice(computer_winning_tiles)
    if len(player_winning_tiles) != 0:
        return random.choice(player_winning_tiles)
    should_computer_put_tile_next_to_player = random.choice([True, False])
    if should_computer_put_tile_next_to_player:
        return make_easy_computer_turn(hexagons, empty_tiles, computer_color)
    return make_hard_computer_turn(hexagons, computer_color)
