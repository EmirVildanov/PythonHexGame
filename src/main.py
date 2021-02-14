import pygame
import pygame.freetype
import time
import random

from gameState import GameState
from intersectionCoordinator import is_inside_polygon
from constants import RED, BLUE, WHITE, FIELD_SIZE, BLACK, FIELD_SIDE, H1, SIDE, H2, GREEN, APP_NAME, SCREEN_WIDTH, \
    SCREEN_HEIGHT, APP_FONT
from tile import Tile


def draw_hexagon_borders(coordinates):
    for i in range(len(coordinates) - 1):
        pygame.draw.line(screen, BLACK, coordinates[i], coordinates[i + 1], 1)


def draw_game_field_borders():
    borders_width = 10
    pygame.draw.rect(screen, RED, [0, 0, FIELD_SIDE * 2 * H1, borders_width])
    pygame.draw.rect(screen, RED, [H1 * (FIELD_SIDE - 1), SCREEN_HEIGHT - borders_width, SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.draw.polygon(screen, BLUE,
                        [(0, borders_width), (H1 * (FIELD_SIDE - 1) + H1, SCREEN_HEIGHT),
                         (H1 * (FIELD_SIDE - 1), SCREEN_HEIGHT),
                         (0, borders_width + H1)])
    pygame.draw.polygon(screen, BLUE, [((FIELD_SIDE * 2 - 1) * H1, 0), (SCREEN_WIDTH, SCREEN_HEIGHT),
                                       (SCREEN_WIDTH + H1, SCREEN_HEIGHT),
                                       (FIELD_SIDE * 2 * H1, 0)])


def draw_tiles():
    for i in range(FIELD_SIZE):
        pygame.draw.polygon(screen, hexagons[i].color, hexagons[i].coordinates)
        draw_hexagon_borders(hexagons[i].coordinates)
        text_surface = game_font.render(str(i), False, (0, 0, 0), WHITE)
        screen.blit(text_surface, (hexagons[i].coordinates[0][0] - 10, hexagons[i].coordinates[0][1] + 10))


def define_hexagon_border_indices(hexagon_border_index, i_index, j_index):
    test_list = []
    if j_index == 0:
        hexagon_border_index.append(0)
    elif j_index == FIELD_SIDE - 1:
        hexagon_border_index.append(2)
    if i_index == 0:
        hexagon_border_index.append(1)
    elif i_index == FIELD_SIDE - 1:
        hexagon_border_index.append(3)


def define_hexagon_neighbours_indices(hexagon_neighbours_indices, i_index, j_index):
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


def get_hexagon_coordinates(upper_x, upper_y, hexagon_side, h1, h2):
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


def initialize_field(hexagons_list):
    first_hexagon_upper_x = H1
    first_hexagon_upper_y = 0
    for i in range(FIELD_SIDE):
        for j in range(FIELD_SIDE):
            current_hexagon_border_indices = []
            current_hexagon_neighbors_indices = []

            define_hexagon_border_indices(current_hexagon_border_indices, i, j)
            define_hexagon_neighbours_indices(current_hexagon_neighbors_indices, i, j)

            current_upper_x_coordinate = first_hexagon_upper_x + (i * H1) + (j * H1 * 2)
            current_upper_y_coordinate = first_hexagon_upper_y + (i * SIDE * 3 / 2.)
            current_hexagon_coordinates = get_hexagon_coordinates(current_upper_x_coordinate,
                                                                  current_upper_y_coordinate, SIDE, H1, H2)
            hexagons_list.append(
                Tile(WHITE, current_hexagon_coordinates, current_hexagon_neighbors_indices,
                     current_hexagon_border_indices))


def initialize_screen():
    pygame.init()
    game_image = pygame.image.load('hex.png')
    pygame.display.set_caption(APP_NAME)
    pygame.display.set_icon(game_image)
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def make_turn(player_color, is_running):
    hexagons[hovered_hexagon_index].color = player_color
    game_winner = check_winner(hovered_hexagon_index, player_color)
    if player_color == BLUE:
        player_color = RED
    else:
        player_color = BLUE
    if game_winner != WHITE:
        is_running = False
    return player_color, is_running, game_winner


# may unite two functions
def make_computer_turn(player_color, is_running):
    empty_tiles = [hexagon for hexagon in hexagons if hexagon.color == WHITE]
    computer_tile_index = random.choice(empty_tiles)
    computer_tile_index.color = player_color
    game_winner = check_winner(hovered_hexagon_index, player_color)
    if player_color == BLUE:
        player_color = RED
    else:
        player_color = BLUE
    if game_winner != WHITE:
        is_running = False
    return player_color, is_running, game_winner


def visit_neighbours(index, visiting_list, borders_list, color):
    current_hexagon = hexagons[index]
    current_hexagon_have_unvisited_neighbours = False  # unvisited neighbours of given color
    for neighbour_index in current_hexagon.neighbours_indices:
        if not visiting_list[neighbour_index] and hexagons[neighbour_index].color == color:
            current_hexagon_have_unvisited_neighbours = True
            break
    visiting_list[index] = True
    borders_list.extend(hexagons[index].border_indices)
    if current_hexagon_have_unvisited_neighbours:
        for neighbour_index in current_hexagon.neighbours_indices:
            if not visiting_list[neighbour_index] and hexagons[neighbour_index].color == color:
                visit_neighbours(neighbour_index, visiting_list, borders_list, color)


def find_game_winner(borders_list, color):
    if color == BLUE and (0 in borders_list and 2 in borders_list):
        return BLUE
    elif color == RED and (1 in borders_list and 3 in borders_list):
        return RED
    return WHITE


def check_winner(index, color):
    hexagons_visiting_list = [False for _ in range(FIELD_SIZE)]
    visited_borders_list = []
    visit_neighbours(index, hexagons_visiting_list, visited_borders_list, color)
    game_winner = find_game_winner(visited_borders_list, color)
    return game_winner


def handle_game_event(is_running, player_color, hovered_hexagon_index, event):
    game_winner = WHITE
    if event.type == pygame.QUIT:
        is_running = False
    if event.type == pygame.MOUSEMOTION:
        for i in range(len(hexagons)):
            if is_inside_polygon(hexagons[i].coordinates, pygame.mouse.get_pos()):
                hovered_hexagon_index = i
    if event.type == pygame.MOUSEBUTTONDOWN:
        if hovered_hexagon_index != -1 and hexagons[hovered_hexagon_index].color == WHITE:
            player_color, is_running, game_winner = make_turn(player_color, is_running)
            if is_computer_on and game_winner == WHITE:
                # time.sleep(0.5)
                player_color, is_running, game_winner = make_computer_turn(player_color, is_running)
    return is_running, player_color, hovered_hexagon_index, game_winner


def blit_text_at_centered_coordinates(text, font, center_x, center_y, color, background):
    text_object = font.render(text, True, color, background)
    text_surface, text_rectangle = text_object, text_object.get_rect()
    text_rectangle.center = (center_x, center_y)
    screen.blit(text_surface, text_rectangle)


def message_winner_to_screen(color):
    screen.fill(WHITE)
    if color == WHITE:
        return
    elif color == BLUE:
        text = "Blue won!"
    else:
        text = "Red won!"
    blit_text_at_centered_coordinates(text, won_font, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, color, WHITE)
    pygame.display.update()
    time.sleep(3)


if __name__ == '__main__':
    running = True
    next_player_color = BLUE
    is_computer_on = False
    game_state = GameState.MENU

    hexagons = []
    initialize_field(hexagons)
    screen = initialize_screen()
    game_font = pygame.font.SysFont(APP_FONT, 10)
    buttons_font = pygame.font.SysFont(APP_FONT, 15)
    won_font = pygame.font.SysFont(APP_FONT, 50)

    hovered_hexagon_index = -1
    hovered_menu_button_index = -1  # 1 - without computer, 2 - with computer
    screen.fill(WHITE)
    button_width = 150
    button_height = 30

    testRect = pygame.Rect((0, 0, 50, 50))

    blit_text_at_centered_coordinates("Welcome to HEX game!", won_font, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5, BLUE,
                                      WHITE)
    blit_text_at_centered_coordinates("choose game mode:", won_font, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5 * 2, BLACK,
                                      WHITE)

    buttons_y = SCREEN_HEIGHT / 5 * 3
    button1_x = SCREEN_WIDTH / 5
    p1 = (button1_x, buttons_y)
    p2 = (button1_x + button_width, buttons_y)
    p3 = (button1_x + button_width, buttons_y + button_width)
    p4 = (button1_x, buttons_y + button_width)
    button1_coordinates = [p1, p2, p3, p4]
    pygame.draw.rect(screen, GREEN, [button1_x, buttons_y, button_width, button_height])

    blit_text_at_centered_coordinates("Without computer", buttons_font, button1_x + button_width / 2,
                                      buttons_y + button_height / 2, BLACK, GREEN)

    button2_x = SCREEN_WIDTH / 5 * 3
    q1 = (button2_x, buttons_y)
    q2 = (button2_x + button_width, buttons_y)
    q3 = (button2_x + button_width, buttons_y + button_width)
    q4 = (button2_x, buttons_y + button_width)
    button2_coordinates = [q1, q2, q3, q4]
    pygame.draw.rect(screen, RED, [button2_x, buttons_y, button_width, button_height])

    blit_text_at_centered_coordinates("With computer", buttons_font, button2_x + button_width / 2,
                                      buttons_y + button_height / 2, BLACK, RED)

    pygame.display.update()

    while game_state == GameState.MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = GameState.IN_PROGRESS
                running = False
            if event.type == pygame.MOUSEMOTION:
                if is_inside_polygon(button1_coordinates, pygame.mouse.get_pos()):
                    hovered_menu_button_index = 1
                elif is_inside_polygon(button2_coordinates, pygame.mouse.get_pos()):
                    hovered_menu_button_index = 2
                else:
                    hovered_menu_button_index = -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hovered_menu_button_index == 1:
                    is_computer_on = False
                    game_state = GameState.IN_PROGRESS
                if hovered_menu_button_index == 2:
                    is_computer_on = True
                    game_state = GameState.IN_PROGRESS

    screen.fill(WHITE)
    draw_game_field_borders()
    winner = WHITE
    while running:
        draw_tiles()

        for event in pygame.event.get():
            running, next_player_color, hovered_hexagon_index, winner = handle_game_event(running, next_player_color,
                                                                                          hovered_hexagon_index, event)

        if hovered_hexagon_index != -1:
            pygame.draw.polygon(screen, GREEN, hexagons[hovered_hexagon_index].coordinates)
        pygame.display.update()

    message_winner_to_screen(winner)
