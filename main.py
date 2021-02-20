from typing import Sequence, List, Tuple, Union

import pygame
import pygame.freetype
import time

from game_state import GameState
from intersect_coordinator import is_inside_polygon
from constants import *
from bot import Bot, find_best_tile_for_bot, find_game_winner
from tile import Tile


def find_button_coordinates(button_x, buttons_y, button_width, button_height):
    p1 = (button_x, buttons_y)
    p2 = (button_x + button_width, buttons_y)
    p3 = (button_x + button_width, buttons_y + button_height)
    p4 = (button_x, buttons_y + button_height)
    return [p1, p2, p3, p4]


def blit_text_at_centered_coordinates(screen, text: str,
                                      font: pygame.font.Font,
                                      center_x: int, center_y: int,
                                      color: Tuple[int],
                                      background: Tuple[int]):
    """
    Функция, которая рисует текст так, чтобы он был отцентрован
    По указанным координатам
    Как параметры передаются цвет текста и цвет фона
    """
    text_object = font.render(text, True, color, background)
    text_surface, text_rectangle = text_object, text_object.get_rect()
    text_rectangle.center = (center_x, center_y)
    screen.blit(text_surface, text_rectangle)


def message_winner_to_screen(screen, color: Tuple[int]):
    """
    Функция, которая выводит на экран цвет победителя
    """
    winner_text_font = pygame.font.SysFont(APP_FONT, 50)
    screen.fill(WHITE)
    if color == WHITE:
        return
    elif color == BLUE:
        text = "Blue won!"
    else:
        text = "Red won!"
    blit_text_at_centered_coordinates(screen, text, winner_text_font,
                                      SCREEN_WIDTH / 2,
                                      SCREEN_HEIGHT / 2, color, WHITE)
    time.sleep(0.5)
    pygame.display.update()
    time.sleep(2)
    return text


def draw_menu_screen(screen):
    """
    Функция, которая рисует меню игры
    """
    welcome_text_font = pygame.font.SysFont(APP_FONT, 50)
    blit_text_at_centered_coordinates(screen, "Welcome to HEX game!",
                                      welcome_text_font,
                                      SCREEN_WIDTH / 2,
                                      SCREEN_HEIGHT / 5, BLUE,
                                      WHITE)
    blit_text_at_centered_coordinates(screen, "choose game mode:",
                                      welcome_text_font,
                                      SCREEN_WIDTH / 2,
                                      SCREEN_HEIGHT / 5 * 2, BLACK,
                                      WHITE)

    button_width = 150
    button_height = 30
    buttons_y = SCREEN_HEIGHT / 5 * 3
    button1_x = SCREEN_WIDTH / 5
    button1_coordinates = find_button_coordinates(button1_x, buttons_y,
                                                  button_width, button_height)
    # draw_button_with_text_at_coordinates()
    pygame.draw.rect(screen, GREEN,
                     [button1_x, buttons_y, button_width, button_height])

    blit_text_at_centered_coordinates(screen, "Without computer",
                                      buttons_font,
                                      button1_x + button_width / 2,
                                      buttons_y + button_height / 2, BLACK,
                                      GREEN)

    button2_x = SCREEN_WIDTH / 5 * 3
    button2_coordinates = find_button_coordinates(button2_x, buttons_y,
                                                  button_width, button_height)
    # draw_button_with_text_at_coordinates()
    pygame.draw.rect(screen, RED,
                     [button2_x, buttons_y, button_width, button_height])

    blit_text_at_centered_coordinates(screen, "With computer", buttons_font,
                                      button2_x + button_width / 2,
                                      buttons_y + button_height / 2, BLACK,
                                      RED)

    pygame.display.update()
    return button1_coordinates, button2_coordinates


def draw_hexagon_borders(coordinates: List[List[int]]):
    """
    Функция, которая рисует контцры шестиугольников
    """
    for i in range(len(coordinates) - 1):
        pygame.draw.line(screen, BLACK, coordinates[i], coordinates[i + 1],
                         1)


def find_field_borders_coordinates(borders_width: int):
    """
    Функция, которая возвраает координаты краёв игрового поля
    """
    border0 = [(0, borders_width),
               (H1 * (FIELD_SIDE - 1) + H1, SCREEN_HEIGHT),
               (H1 * (FIELD_SIDE - 1), SCREEN_HEIGHT),
               (0, borders_width + H1)]
    border2 = [((FIELD_SIDE * 2 - 1) * H1, 0),
               (SCREEN_WIDTH, SCREEN_HEIGHT),
               (SCREEN_WIDTH + H1, SCREEN_HEIGHT),
               (FIELD_SIDE * 2 * H1, 0)]
    border1 = [0, 0, FIELD_SIDE * 2 * H1, borders_width]
    border3 = [H1 * (FIELD_SIDE - 1), SCREEN_HEIGHT - borders_width,
               SCREEN_WIDTH, SCREEN_HEIGHT]
    return [border0, border1, border2, border3]


def draw_game_field_borders():
    """
    Функция, которая рисует цветные края поля
    """
    borders_width = HEXAGON_SIDE_IN_PX / 2
    field_borders_coordinates = find_field_borders_coordinates(borders_width)
    pygame.draw.rect(screen, RED, field_borders_coordinates[1])
    pygame.draw.rect(screen, RED, field_borders_coordinates[3])
    pygame.draw.polygon(screen, BLUE, field_borders_coordinates[0])
    pygame.draw.polygon(screen, BLUE, field_borders_coordinates[2])


def draw_tiles():
    """
    Функция, которая рисует шестиугольники
    """
    for i in range(FIELD_SIZE):
        pygame.draw.polygon(screen, hexagons[i].color,
                            hexagons[i].coordinates)
        draw_hexagon_borders(hexagons[i].coordinates)
        text_surface = game_font.render(str(i), False, (0, 0, 0), WHITE)
        screen.blit(text_surface, (hexagons[i].coordinates[0][0] - 10,
                                   hexagons[i].coordinates[0][1] + 10))


def initialize_field() -> Sequence[Tile]:
    """
    Функция, которая возвращает массив из объектов типа
    Tile, которые составляют поле
    """
    hexagons = []
    for i in range(FIELD_SIDE):
        for j in range(FIELD_SIDE):
            hexagons.append(Tile(i, j))
    return hexagons


def initialize_screen():
    """
    Функция, которая создаёт объект screen из библиотеки pygame
    На нём будет рисоваться вся игра
    """
    pygame.init()
    pygame.display.set_caption(APP_NAME)
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def make_turn(hexagons: Sequence[Tile], index: int,
              next_turn_color: Tuple[int], state: GameState,
              is_bot: bool = False):
    """
    Функция, которая:
    Закрашивает указанную клетку, если ходит игрок
    Закрашивает самую удачную для компьютера клетку, если ходит компьютер
    """
    if is_bot:
        best_tile = find_best_tile_for_bot(hexagons, next_turn_color)
        best_tile.set_color(next_turn_color)
        game_winner = find_game_winner(hexagons, best_tile.index,
                                       next_turn_color)
    else:
        hexagons[index].set_color(next_turn_color)
        game_winner = find_game_winner(hexagons, index, next_turn_color)
    if next_turn_color == BLUE:
        next_turn_color = RED
    else:
        next_turn_color = BLUE
    if game_winner != WHITE:
        state = GameState.FINISHED
    return next_turn_color, state, game_winner


def handle_game_event(hexagons: Sequence[Tile],
                      is_bot_on: bool, state: GameState,
                      turn_color: Tuple[int], hovrd_hex_index: int,
                      event: pygame.event.Event):
    """
    Функция, которая обрабатывает движения и нажатия мыши во время игры
    """
    game_winner = WHITE
    if event.type == pygame.QUIT:
        state = GameState.FINISHED
    if event.type == pygame.MOUSEMOTION:
        for i in range(len(hexagons)):
            if is_inside_polygon(hexagons[i].coordinates,
                                 pygame.mouse.get_pos()):
                hovrd_hex_index = i
    if event.type == pygame.MOUSEBUTTONDOWN:
        if hovrd_hex_index != -1 and hexagons[hovrd_hex_index].color == WHITE:
            turn_color, state, game_winner = make_turn(hexagons,
                                                       hovrd_hex_index,
                                                       turn_color, state)
            if is_bot_on and game_winner == WHITE:
                turn_color, state, game_winner = make_turn(
                    hexagons,
                    hovrd_hex_index,
                    turn_color,
                    state,
                    is_bot=True)
    return state, turn_color, hovrd_hex_index, game_winner


def handle_menu_event(state: GameState,
                      is_bot_on: bool,
                      hovered_menu_button_index: int,
                      event: pygame.event.Event):
    """
    Функция, которая обрабатывает движения и нажатия мыши в меню
    """
    if event.type == pygame.QUIT:
        state = GameState.FINISHED
    if event.type == pygame.MOUSEMOTION:
        if is_inside_polygon(with_bot_btn_coordinates,
                             pygame.mouse.get_pos()):
            hovered_menu_button_index = 1
        elif is_inside_polygon(without_bot_btn_coordinates,
                               pygame.mouse.get_pos()):
            hovered_menu_button_index = 2
        else:
            hovered_menu_button_index = -1
    if event.type == pygame.MOUSEBUTTONDOWN:
        if hovered_menu_button_index == 1:
            is_bot_on = False
            state = GameState.IN_PROGRESS
        if hovered_menu_button_index == 2:
            is_bot_on = True
            state = GameState.IN_PROGRESS
    return state, is_bot_on, hovered_menu_button_index


if __name__ == '__main__':
    player_color = BLUE
    turn_color = BLUE
    is_bot_on = False
    bot = Bot(turn_color)
    state = GameState.MENU

    hexagons = initialize_field()
    screen = initialize_screen()
    game_font = pygame.font.SysFont(APP_FONT, 10)
    buttons_font = pygame.font.SysFont(APP_FONT, 15)

    hovered_hex_index = -1
    hvrd_btn_indx = -1  # 1 - without bot, 2 - with bot
    screen.fill(WHITE)

    with_bot_btn_coordinates, without_bot_btn_coordinates = draw_menu_screen(
        screen)

    while state == GameState.MENU:
        for event in pygame.event.get():
            state, is_bot_on, hvrd_btn_indx = handle_menu_event(state,
                                                                is_bot_on,
                                                                hvrd_btn_indx,
                                                                event)
    if state != GameState.FINISHED:
        screen.fill(WHITE)
        draw_game_field_borders()
    winner = WHITE
    while state == GameState.IN_PROGRESS:
        draw_tiles()
        for event in pygame.event.get():
            state, turn_color, hovered_hex_index, winner = handle_game_event(
                hexagons, is_bot_on, state,
                turn_color,
                hovered_hex_index,
                event)
        if hovered_hex_index != -1:
            pygame.draw.polygon(screen, GREEN,
                                hexagons[
                                    hovered_hex_index].coordinates)
        pygame.display.update()
    if winner != WHITE:
        draw_tiles()
        pygame.display.update()
        message_winner_to_screen(screen, winner)
