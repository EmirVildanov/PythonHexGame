from typing import Sequence, List

import pygame
import pygame.freetype
import time

from game_state import GameState
from intersect_coordinator import is_inside_polygon
from constants import *
from bot import Bot, find_best_tile_for_bot, find_game_winner
from tile import Tile


def draw_menu_screen():
    blit_text_at_centered_coordinates("Welcome to HEX game!", won_font, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5, BLUE,
                                      WHITE)
    blit_text_at_centered_coordinates("choose game mode:", won_font, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5 * 2, BLACK,
                                      WHITE)

    button_width = 150
    button_height = 30
    buttons_y = SCREEN_HEIGHT / 5 * 3
    button1_x = SCREEN_WIDTH / 5
    p11 = (button1_x, buttons_y)
    p12 = (button1_x + button_width, buttons_y)
    p13 = (button1_x + button_width, buttons_y + button_width)
    p14 = (button1_x, buttons_y + button_width)
    button1_coordinates = [p11, p12, p13, p14]
    pygame.draw.rect(screen, GREEN, [button1_x, buttons_y, button_width, button_height])

    blit_text_at_centered_coordinates("Without computer", buttons_font, button1_x + button_width / 2,
                                      buttons_y + button_height / 2, BLACK, GREEN)

    button2_x = SCREEN_WIDTH / 5 * 3
    p21 = (button2_x, buttons_y)
    p22 = (button2_x + button_width, buttons_y)
    p23 = (button2_x + button_width, buttons_y + button_width)
    p24 = (button2_x, buttons_y + button_width)
    button2_coordinates = [p21, p22, p23, p24]
    pygame.draw.rect(screen, RED, [button2_x, buttons_y, button_width, button_height])

    blit_text_at_centered_coordinates("With computer", buttons_font, button2_x + button_width / 2,
                                      buttons_y + button_height / 2, BLACK, RED)

    pygame.display.update()
    return button1_coordinates, button2_coordinates


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


def initialize_field():
    hexagons = []
    for i in range(FIELD_SIDE):
        for j in range(FIELD_SIDE):
            hexagons.append(Tile(i, j))
    return hexagons


def initialize_screen():
    pygame.init()
    game_image = pygame.image.load('hex.png')
    pygame.display.set_caption(APP_NAME)
    pygame.display.set_icon(game_image)
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def make_turn(hexagons: Sequence[Tile], index, next_turn_color, is_running, is_computer=False):
    if is_computer:
        best_tile = find_best_tile_for_bot(hexagons, next_turn_color)
        best_tile.set_color(next_turn_color)
        game_winner = find_game_winner(hexagons, best_tile.index, next_turn_color)
    else:
        hexagons[index].set_color(next_turn_color)
        game_winner = find_game_winner(hexagons, index, next_turn_color)
    if next_turn_color == BLUE:
        next_turn_color = RED
    else:
        next_turn_color = BLUE
    if game_winner != WHITE:
        is_running = False
    return next_turn_color, is_running, game_winner


def handle_game_event(is_running, next_turn_color, hovered_hexagon_index, event):
    game_winner = WHITE
    if event.type == pygame.QUIT:
        is_running = False
    if event.type == pygame.MOUSEMOTION:
        for i in range(len(hexagons)):
            if is_inside_polygon(hexagons[i].coordinates, pygame.mouse.get_pos()):
                hovered_hexagon_index = i
    if event.type == pygame.MOUSEBUTTONDOWN:
        if hovered_hexagon_index != -1 and hexagons[hovered_hexagon_index].color == WHITE:
            next_turn_color, is_running, game_winner = make_turn(hexagons, hovered_hexagon_index, next_turn_color,
                                                                 is_running)
            if is_bot_on and game_winner == WHITE:
                next_turn_color, is_running, game_winner = make_turn(hexagons, hovered_hexagon_index, next_turn_color,
                                                                     is_running, is_computer=True)
    return is_running, next_turn_color, hovered_hexagon_index, game_winner


def handle_menu_event(running, is_computer_on, game_state, hovered_menu_button_index, event):
    if event.type == pygame.QUIT:
        game_state = GameState.IN_PROGRESS
        running = False
    if event.type == pygame.MOUSEMOTION:
        if is_inside_polygon(with_computer_button_coordinates, pygame.mouse.get_pos()):
            hovered_menu_button_index = 1
        elif is_inside_polygon(without_computer_button_coordinates, pygame.mouse.get_pos()):
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
    return running, is_computer_on, game_state, hovered_menu_button_index


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
    time.sleep(0.5)
    pygame.display.update()
    time.sleep(2)


if __name__ == '__main__':
    running = True
    player_color = BLUE
    next_turn_color = BLUE
    is_bot_on = False
    bot = Bot(next_turn_color)
    game_state = GameState.MENU

    hexagons = initialize_field()
    screen = initialize_screen()
    game_font = pygame.font.SysFont(APP_FONT, 10)
    buttons_font = pygame.font.SysFont(APP_FONT, 15)
    won_font = pygame.font.SysFont(APP_FONT, 50)

    hovered_hexagon_index = -1
    hovered_menu_button_index = -1  # 1 - without bot, 2 - with bot
    screen.fill(WHITE)

    with_computer_button_coordinates, without_computer_button_coordinates = draw_menu_screen()

    while game_state == GameState.MENU:
        for event in pygame.event.get():
            running, is_bot_on, game_state, hovered_menu_button_index = handle_menu_event(running, is_bot_on,
                                                                                          game_state,
                                                                                          hovered_menu_button_index,
                                                                                          event)

    screen.fill(WHITE)
    draw_game_field_borders()
    winner = WHITE
    while running:
        draw_tiles()

        for event in pygame.event.get():
            running, next_turn_color, hovered_hexagon_index, winner = handle_game_event(running, next_turn_color,
                                                                                        hovered_hexagon_index,
                                                                                        event)
        if hovered_hexagon_index != -1:
            pygame.draw.polygon(screen, GREEN, hexagons[hovered_hexagon_index].coordinates)
        pygame.display.update()
    draw_tiles()
    pygame.display.update()
    # if winner != player_color:
    #     time.sleep(0.5)
    message_winner_to_screen(winner)
