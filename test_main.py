from main import *
from bot import find_opposite_color


def test_should_return_correct_menu_button_coordinates():
    button_width = 150
    button_height = 30
    buttons_y = SCREEN_HEIGHT / 5 * 3
    button1_x = SCREEN_WIDTH / 5
    assert [
        (110.8, 204.0),
        (260.8, 204.0),
        (260.8, 234.0),
        (110.8, 234.0),
    ] == find_button_coordinates(button1_x, buttons_y, button_width, button_height)


def test_should_find_field_border_coordinates():
    border_width = 3
    correct_border_coordinates = [0, 0, FIELD_SIDE * 2 * H1, border_width]
    border_coordinates = find_field_borders_coordinates(border_width)[1]
    assert correct_border_coordinates == border_coordinates


def test_should_find_opposite_color_of_red():
    color = find_opposite_color(RED)
    assert color == BLUE


def test_assert_that_created_list_of_tiles_with_size_of_field_size():
    hexagons = initialize_field()
    assert len(hexagons) == FIELD_SIZE
    for item in hexagons:
        assert type(item) is Tile


def test_should_assert_that_red_is_winner():
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
    make_turn(hexagons, turn_tile_index, turn_color, GameState.IN_PROGRESS)
    assert hexagons[0].color == turn_color


def test_should_correctly_react_on_mouse_click_during_the_game():
    hexagons = initialize_field()
    state = GameState.IN_PROGRESS
    is_bot_on = False
    turn_color = BLUE
    filling_line_index = 3
    winner_color = BLUE
    for j in range(FIELD_SIDE - 1):
        current_tile_index = filling_line_index * FIELD_SIDE + j
        hexagons[current_tile_index].color = winner_color
    winning_tile_index = filling_line_index * FIELD_SIDE + (FIELD_SIDE - 1)
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"pos": (375, 214), "button": 1, "window": None}
    )
    state, turn_color, _, winner = handle_game_event(
        hexagons, is_bot_on, state, turn_color, winning_tile_index, event
    )
    assert GameState.FINISHED is state
    assert RED == turn_color
    assert BLUE == winner


def test_should_correctly_react_on_mouse_click_during_the_menu():
    hexagons = initialize_field()
    state = GameState.MENU
    is_bot_on = False
    state = GameState.MENU
    turn_color = BLUE
    filling_line_index = 3
    winner_color = BLUE
    for j in range(FIELD_SIDE - 1):
        current_tile_index = filling_line_index * FIELD_SIDE + j
        hexagons[current_tile_index].color = winner_color
    hovered_btn_index = 2
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"pos": (403, 218), "button": 1, "window": None}
    )
    state, is_bot_on, _ = handle_menu_event(state, is_bot_on, hovered_btn_index, event)
    assert GameState.IN_PROGRESS is state
    assert True is is_bot_on
    assert GameState.IN_PROGRESS == state
