from main import *
from bot import *


def test_should_say_that_red_is_winner():
    hexagons = initialize_field()
    filling_line_index = 3
    winner_color = BLUE
    for j in range(FIELD_SIDE - 1):
        current_tile_index = filling_line_index * FIELD_SIDE + j
        hexagons[current_tile_index].color = winner_color
    winning_tile_index = filling_line_index * FIELD_SIDE + (FIELD_SIDE - 1)
    winner = find_game_winner(hexagons, winning_tile_index, winner_color)
    assert winner == BLUE


def test_should_assert_returning_correct_visiting_list():
    hexagons = initialize_field()
    color = BLUE
    visit = [False for _ in range(FIELD_SIZE)]
    asserting_visit = [False for _ in range(FIELD_SIZE)]
    colored_tiles_block_indices = [0, 1, 2, 13, 23, 24]
    correct_visiting_indices = [0, 1, 2, 13, 23, 24]
    for index in correct_visiting_indices:
        asserting_visit[index] = True
    for index in colored_tiles_block_indices:
        hexagons[index].set_color(color)
    assert asserting_visit == visit_neighbours(hexagons, 0, visit, color)


def test_should_find_correct_opposite_color():
    assert find_opposite_color(RED) == BLUE


def test_should_find_correct_neighbours():
    hexagons = initialize_field()
    colored_tiles_block_indices = [0, 1, 2, 13, 23, 24]
    colored_tiles_block = [hexagon for hexagon in hexagons if
                           hexagon.index in colored_tiles_block_indices]
    correct_neighbours_indices = [0, 1, 2, 13, 23, 24, 11, 12, 22, 33, 34, 35, 25, 14, 3]
    answer_tiles_indices = [tile.index for tile in find_neighbour_tiles(hexagons,
                                                              colored_tiles_block)]
    for index in correct_neighbours_indices:
        assert index in answer_tiles_indices
