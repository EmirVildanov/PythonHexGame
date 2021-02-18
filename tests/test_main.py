from src.constants import *
from src.main import *


def test_should_find_opposite_color_of_red():
    color = find_opposite_color(RED)
    assert color == BLUE

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


def test_should_make_player_turn():
    hexagons = initialize_field()
    turn_tile_index = 0
    turn_color = BLUE
    make_turn(hexagons, turn_tile_index, turn_color, True)
    assert hexagons[0].color == turn_color
