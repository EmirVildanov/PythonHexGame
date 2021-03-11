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
    assert winner == winner_color


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
    colored_tiles_block = [
        hexagon for hexagon in hexagons if hexagon.index in colored_tiles_block_indices
    ]
    correct_neighbours_indices = [
        0,
        1,
        2,
        13,
        23,
        24,
        11,
        12,
        22,
        33,
        34,
        35,
        25,
        14,
        3,
    ]
    answer_tiles_indices = [
        tile.index for tile in find_neighbour_tiles(hexagons, colored_tiles_block)
    ]
    for index in correct_neighbours_indices:
        assert index in answer_tiles_indices


def test_should_find_correct_winning_tiles_for_color():
    hexagons = initialize_field()
    filling_line_index = 3
    winner_color = BLUE
    for j in range(FIELD_SIDE - 1):
        current_tile_index = filling_line_index * FIELD_SIDE + j
        hexagons[current_tile_index].color = winner_color
    empty_tiles = [hexagon for hexagon in hexagons if hexagon.color == WHITE]
    winning_tiles = find_winning_tiles_for_color(hexagons, empty_tiles, winner_color)
    correct_winning_tiles_indices = [32, 43]
    for winning_tiles in winning_tiles:
        assert winning_tiles.index in correct_winning_tiles_indices


def test_should_find_concrete_border_tiles():
    hexagons = initialize_field()
    color = BLUE
    colored_tiles_indices = [22, 23, 66]
    for index in colored_tiles_indices:
        hexagons[index].set_color(color)
    border0_tiles = [hexagon for hexagon in hexagons if 0 in hexagon.border_indices]
    border0_tiles = find_concrete_border_tiles(hexagons, border0_tiles, color)
    correct_border_tile_indices = [
        0,
        11,
        12,
        13,
        24,
        34,
        33,
        44,
        55,
        56,
        67,
        77,
        88,
        99,
        110,
    ]
    for tile in border0_tiles:
        assert tile.index in correct_border_tile_indices


def test_should_find_field_border_tiles():
    hexagons = initialize_field()
    color = BLUE
    colored_tiles_indices = [22, 23, 66, 10]
    for index in colored_tiles_indices:
        hexagons[index].set_color(color)
    border1_tiles, border2_tiles = find_field_border_tiles(hexagons, color)
    correct_border1_tile_indices = [
        0,
        11,
        12,
        13,
        24,
        34,
        33,
        44,
        55,
        56,
        67,
        77,
        88,
        99,
        110,
    ]
    correct_border2_tile_indices = [9, 20, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120]
    for tile in border1_tiles:
        assert tile.index in correct_border1_tile_indices
    for tile in border2_tiles:
        assert tile.index in correct_border2_tile_indices


def test_should_find_some_distances_from_given_tile_to_other():
    hexagons = initialize_field()
    tile = hexagons[0]
    distance_from_tile1_to_all_tiles = find_all_distances_from_tile(hexagons, tile)
    assert -1 == distance_from_tile1_to_all_tiles[0]
    assert 1 == distance_from_tile1_to_all_tiles[1]
    assert 9 == distance_from_tile1_to_all_tiles[9]
    assert 1 == distance_from_tile1_to_all_tiles[11]
    assert 20 == distance_from_tile1_to_all_tiles[FIELD_SIZE - 1]


def test_should_find_neighbours_of_not_opposite_color():
    hexagons = initialize_field()
    color = RED
    opposite_color = BLUE
    tile = hexagons[11]
    opposite_colored_tiles_block_indices = [0, 1, 2]
    for index in opposite_colored_tiles_block_indices:
        hexagons[index].set_color(opposite_color)
    hexagons[12].set_color(RED)
    correct_neighbours_indices = [12, 22]
    answer_tiles_indices = [
        tile.index
        for tile in find_neighbours_of_not_opposite_color(hexagons, tile, color)
    ]
    for index in correct_neighbours_indices:
        assert index in answer_tiles_indices


def test_should_find_path_from_tile_to_tile():
    hexagons = initialize_field()
    path = find_path_from_tile_to_tile(hexagons, hexagons[0], hexagons[110])
    correct_path = [hexagons[i * 11] for i in range(FIELD_SIDE)]
    assert correct_path == path


def test_should_recommend_not_player_winning_tile_for_bot():
    hexagons = initialize_field()
    filling_line_index = 0
    winner_color = BLUE
    for j in range(FIELD_SIDE - 1):
        current_tile_index = filling_line_index * FIELD_SIDE + j
        hexagons[current_tile_index].color = winner_color
    winning_tile_index = filling_line_index * FIELD_SIDE + (FIELD_SIDE - 1)
    best_tile = find_best_tile_for_bot(hexagons, RED)
    assert winning_tile_index == best_tile.index
