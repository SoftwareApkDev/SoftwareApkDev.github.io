"""
This file contains code for the game "Life Simulation".
Author: SoftwareApkDev

The game "Life Simulation" is inspired by "Stardew Valley" (https://www.stardewvalley.net/) and
"Torn RPG" (https://www.torn.com/).
"""


# Game version: 1


# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import random
from datetime import datetime, timedelta
import os
from functools import reduce

import mpmath
from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True


# Creating static variables to be used throughout the game.


LETTERS: str = "abcdefghijklmnopqrstuvwxyz"
ELEMENT_CHART: list = [
    ["ATTACKING\nELEMENT", "TERRA", "FLAME", "SEA", "NATURE", "ELECTRIC", "ICE", "METAL", "DARK", "LIGHT", "WAR",
     "PURE",
     "LEGEND", "PRIMAL", "WIND"],
    ["DOUBLE\nDAMAGE", "ELECTRIC\nDARK", "NATURE\nICE", "FLAME\nWAR", "SEA\nLIGHT", "SEA\nMETAL", "NATURE\nWAR",
     "TERRA\nICE", "METAL\nLIGHT", "ELECTRIC\nDARK", "TERRA\nFLAME", "LEGEND", "PRIMAL", "PURE", "WIND"],
    ["HALF\nDAMAGE", "METAL\nWAR", "SEA\nWAR", "NATURE\nELECTRIC", "FLAME\nICE", "TERRA\nLIGHT", "FLAME\nMETAL",
     "ELECTRIC\nDARK", "TERRA", "NATURE", "SEA\nICE", "PRIMAL", "PURE", "LEGEND", "N/A"],
    ["NORMAL\nDAMAGE", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER", "OTHER",
     "OTHER",
     "OTHER", "OTHER", "OTHER"]
]


# Creating static functions to be used throughout the game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def tabulate_element_chart() -> str:
    return str(tabulate(ELEMENT_CHART, headers='firstrow', tablefmt='fancy_grid'))


def generate_random_name() -> str:
    return "".join([LETTERS[random.randint(0, len(LETTERS) - 1)] for i in range(random.randint(5, 25))]).capitalize()


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


def get_elemental_damage_multiplier(element1: str, element2: str) -> mpf:
    if element1 == "TERRA":
        return mpf("2") if element2 in ["ELECTRIC, DARK"] else mpf("0.5") if element2 in ["METAL", "WAR"] else mpf("1")
    elif element1 == "FLAME":
        return mpf("2") if element2 in ["NATURE", "ICE"] else mpf("0.5") if element2 in ["SEA", "WAR"] else mpf("1")
    elif element1 == "SEA":
        return mpf("2") if element2 in ["FLAME", "WAR"] else mpf("0.5") if element2 in ["NATURE", "ELECTRIC"] else \
            mpf("1")
    elif element1 == "NATURE":
        return mpf("2") if element2 in ["SEA", "LIGHT"] else mpf("0.5") if element2 in ["FLAME", "ICE"] else mpf("1")
    elif element1 == "ELECTRIC":
        return mpf("2") if element2 in ["SEA", "METAL"] else mpf("0.5") if element2 in ["TERRA", "LIGHT"] else mpf("1")
    elif element1 == "ICE":
        return mpf("2") if element2 in ["NATURE", "WAR"] else mpf("0.5") if element2 in ["FLAME", "METAL"] else mpf("1")
    elif element1 == "METAL":
        return mpf("2") if element2 in ["TERRA", "ICE"] else mpf("0.5") if element2 in ["ELECTRIC", "DARK"] else \
            mpf("1")
    elif element1 == "DARK":
        return mpf("2") if element2 in ["METAL", "LIGHT"] else mpf("0.5") if element2 == "TERRA" else mpf("1")
    elif element1 == "LIGHT":
        return mpf("2") if element2 in ["ELECTRIC", "DARK"] else mpf("0.5") if element2 == "NATURE" else mpf("1")
    elif element1 == "WAR":
        return mpf("2") if element2 in ["TERRA", "FLAME"] else mpf("0.5") if element2 in ["SEA", "ICE"] else mpf("1")
    elif element1 == "PURE":
        return mpf("2") if element2 == "LEGEND" else mpf("0.5") if element2 == "PRIMAL" else mpf("1")
    elif element1 == "LEGEND":
        return mpf("2") if element2 == "PRIMAL" else mpf("0.5") if element2 == "PURE" else mpf("1")
    elif element1 == "PRIMAL":
        return mpf("2") if element2 == "PURE" else mpf("0.5") if element2 == "LEGEND" else mpf("1")
    elif element1 == "WIND":
        return mpf("2") if element2 == "WIND" else mpf("1")
    else:
        return mpf("1")


def resistance_accuracy_rule(accuracy: mpf, resistance: mpf) -> mpf:
    if resistance - accuracy <= mpf("0.15"):
        return mpf("0.15")
    else:
        return resistance - accuracy


def load_game_data(file_name):
    # type: (str) -> Game
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (Game, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes to be used throughout the game.


###########################################
# MINIGAMES
###########################################


class Minigame:
    """
    This class contains attributes of a minigame in this game.
    """

    POSSIBLE_NAMES: list = ["BOX EATS PLANTS", "MATCH WORD PUZZLE", "MATCH-3 GAME"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]
        self.already_played: bool = False

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Minigame
        return copy.deepcopy(self)


###########################################
# MINIGAMES
###########################################


###########################################
# BOX EATS PLANTS
###########################################


class BoxEatsPlantsBoard:
    """
    This class contains attributes of a board in the game "Box Eats Plants".
    """

    BOARD_WIDTH: int = 10
    BOARD_HEIGHT: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                new.append(BoxEatsPlantsTile())

            self.__tiles.append(new)

    def num_plants(self):
        # type: () -> int
        plants: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: BoxEatsPlantsTile = self.get_tile_at(x, y)
                if isinstance(curr_tile.plant, Plant):
                    plants += 1

        return plants

    def num_rocks(self):
        # type: () -> int
        rocks: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: BoxEatsPlantsTile = self.get_tile_at(x, y)
                if isinstance(curr_tile.rock, Rock):
                    rocks += 1

        return rocks

    def num_boxes(self):
        # type: () -> int
        boxes: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: BoxEatsPlantsTile = self.get_tile_at(x, y)
                if isinstance(curr_tile.box, Box):
                    boxes += 1

        return boxes

    def spawn_plant(self):
        # type: () -> Plant
        plant_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        plant_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        plant_tile: BoxEatsPlantsTile = self.__tiles[plant_y][plant_x]
        while plant_tile.plant is not None:
            plant_x = random.randint(0, self.BOARD_WIDTH - 1)
            plant_y = random.randint(0, self.BOARD_HEIGHT - 1)
            plant_tile = self.__tiles[plant_y][plant_x]

        plant: Plant = Plant(plant_x, plant_y)
        plant_tile.add_plant(plant)
        return plant

    def spawn_rock(self):
        # type: () -> Rock
        rock_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        rock_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        rock_tile: BoxEatsPlantsTile = self.__tiles[rock_y][rock_x]
        while rock_tile.rock is not None:
            rock_x = random.randint(0, self.BOARD_WIDTH - 1)
            rock_y = random.randint(0, self.BOARD_HEIGHT - 1)
            rock_tile = self.__tiles[rock_y][rock_x]

        rock: Rock = Rock(rock_x, rock_y)
        rock_tile.add_rock(rock)
        return rock

    def spawn_box(self):
        # type: () -> Box
        box_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        box_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        box_tile: BoxEatsPlantsTile = self.__tiles[box_y][box_x]
        while box_tile.plant is not None or box_tile.rock is not None:
            box_x = random.randint(0, self.BOARD_WIDTH - 1)
            box_y = random.randint(0, self.BOARD_HEIGHT - 1)
            box_tile = self.__tiles[box_y][box_x]
        box: Box = Box(box_x, box_y)
        box_tile.add_box(box)
        return box

    def get_tile_at(self, x, y):
        # type: (int, int) -> BoxEatsPlantsTile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> BoxEatsPlantsBoard
        return copy.deepcopy(self)


class Box:
    """
    This class contains attributes of a box in the game "Box Eats Plants".
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "BOX"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.y -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_down(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.y += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_left(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.x -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_right(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.x += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Box
        return copy.deepcopy(self)


class Plant:
    """
    This class contains attributes of a plant in the game "Box Eats Plants".
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "PLANT"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.y -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_down(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.y += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_left(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.x -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_right(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.x += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Plant
        return copy.deepcopy(self)


class Rock:
    """
    This class contains attributes of a rock in the game "Box Eats Plants".
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "ROCK"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.y -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_down(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.y += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_left(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x > 0:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.x -= 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_right(self, board):
        # type: (BoxEatsPlantsBoard) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.x += 1
            new_tile: BoxEatsPlantsTile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Rock
        return copy.deepcopy(self)


class BoxEatsPlantsTile:
    """
    This class contains attributes of a tile in the minigame "Box Eats Plants".
    """

    def __init__(self):
        # type: () -> None
        self.box: Box or None = None
        self.plant: Plant or None = None
        self.rock: Rock or None = None

    def add_box(self, box):
        # type: (Box) -> bool
        if self.box is None:
            self.box = box
            return True
        return False

    def remove_box(self):
        # type: () -> None
        self.box = None

    def add_plant(self, plant):
        # type: (Plant) -> bool
        if self.plant is None:
            self.plant = plant
            return True
        return False

    def remove_plant(self):
        # type: () -> None
        self.plant = None

    def add_rock(self, rock):
        # type: (Rock) -> bool
        if self.rock is None:
            self.rock = rock
            return True
        return False

    def remove_rock(self):
        # type: () -> None
        self.rock = None

    def __str__(self):
        # type: () -> str
        if self.box is None and self.plant is None and self.rock is None:
            return "NONE"
        res: str = ""  # initial value
        if isinstance(self.box, Box):
            res += str(self.box)

        if isinstance(self.plant, Plant):
            if self.box is not None:
                res += "\n" + str(self.plant)
            else:
                res += str(self.plant)

        if isinstance(self.rock, Rock):
            if self.box is not None or self.plant is not None:
                res += "\n" + str(self.rock)
            else:
                res += str(self.rock)

        return res

    def clone(self):
        # type: () -> BoxEatsPlantsTile
        return copy.deepcopy(self)


###########################################
# BOX EATS PLANTS
###########################################


###########################################
# MATCH WORD PUZZLE
###########################################


def get_index_of_element(a_list: list, elem: object) -> int:
    for i in range(len(a_list)):
        if a_list[i] == elem:
            return i

    return -1


class MatchWordPuzzleBoard:
    """
    This class contains attributes of the board for the minigame "Match Word Puzzle".
    """

    BOARD_WIDTH: int = 6
    BOARD_HEIGHT: int = 4

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        chosen_keywords: list = []  # initial value
        chosen_keywords_tally: list = [0] * 12
        for i in range(12):
            curr_keyword: str = MatchWordPuzzleTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                     len(MatchWordPuzzleTile.POSSIBLE_KEYWORDS) - 1)]
            while curr_keyword in chosen_keywords:
                curr_keyword = MatchWordPuzzleTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                    len(MatchWordPuzzleTile.POSSIBLE_KEYWORDS) - 1)]

            chosen_keywords.append(curr_keyword)

        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                curr_keyword: str = chosen_keywords[random.randint(0, len(chosen_keywords) - 1)]
                while chosen_keywords_tally[get_index_of_element(chosen_keywords, curr_keyword)] >= 2:
                    curr_keyword = chosen_keywords[random.randint(0, len(chosen_keywords) - 1)]

                new.append(MatchWordPuzzleTile(curr_keyword))
                chosen_keywords_tally[get_index_of_element(chosen_keywords, curr_keyword)] += 1

            self.__tiles.append(new)

    def all_opened(self):
        # type: () -> bool
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if self.__tiles[i][j].is_closed:
                    return False

        return True

    def get_tile_at(self, x, y):
        # type: (int, int) -> MatchWordPuzzleTile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> MatchWordPuzzleBoard
        return copy.deepcopy(self)


class MatchWordPuzzleTile:
    """
    This class contains attributes of a tile in the minigame "Match Word Puzzle".
    """

    POSSIBLE_KEYWORDS: list = ["AND", "AS", "ASSERT", "BREAK", "CLASS", "CONTINUE", "DEF", "DEL", "ELIF", "ELSE",
                               "EXCEPT", "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL", "IF", "IMPORT", "IN", "IS",
                               "LAMBDA", "NONE", "NONLOCAL", "NOT", "OR", "PASS", "RAISE", "RETURN", "TRUE",
                               "TRY", "WHILE", "WITH", "YIELD"]

    def __init__(self, contents):
        # type: (str) -> None
        self.contents: str = contents if contents in self.POSSIBLE_KEYWORDS else self.POSSIBLE_KEYWORDS[0]
        self.is_closed: bool = True

    def open(self):
        # type: () -> bool
        if self.is_closed:
            self.is_closed = False
            return True
        return False

    def __str__(self):
        # type: () -> str
        return "CLOSED" if self.is_closed else str(self.contents)

    def clone(self):
        # type: () -> MatchWordPuzzleTile
        return copy.deepcopy(self)


###########################################
# MATCH WORD PUZZLE
###########################################


###########################################
# MATCH-3 GAME
###########################################


"""
Code for match-3 game is inspired by the following sources:
1. https://www.raspberrypi.com/news/make-a-columns-style-tile-matching-game-wireframe-25/
2. https://github.com/Wireframe-Magazine/Wireframe-25/blob/master/match3.py
"""


class MatchThreeBoard:
    """
    This class contains attributes of the board for the minigame "Match-3 Game".
    """

    BOARD_WIDTH: int = 10
    BOARD_HEIGHT: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = [["AND"] * self.BOARD_WIDTH for k in range(self.BOARD_HEIGHT)]  # initial value
        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                curr_keyword: str = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                    len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]
                while (i > 0 and self.__tiles[i][j].contents == self.__tiles[i - 1][j].contents) or \
                        (j > 0 and self.__tiles[i][j].contents == self.__tiles[i][j - 1].contents):
                    curr_keyword = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                   len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]

                new.append(MatchThreeTile(curr_keyword))

            self.__tiles.append(new)

        self.__matches: list = []  # initial value

    def swap_tiles(self, x1, y1, x2, y2):
        # type: (int, int, int, int) -> bool
        if self.get_tile_at(x1, y1) is None or self.get_tile_at(x2, y2) is None:
            return False

        temp: MatchThreeTile = self.__tiles[y1][x1]
        self.__tiles[y1][x1] = self.__tiles[y2][x2]
        self.__tiles[y2][x2] = temp
        return True

    def no_possible_moves(self):
        # type: () -> bool
        # Trying all possible moves and checking whether it has matches or not
        for j in range(self.BOARD_WIDTH):
            for i in range(self.BOARD_HEIGHT - 1):
                new_board: MatchThreeBoard = self.clone()
                temp: MatchThreeTile = new_board.__tiles[i][j]
                new_board.__tiles[i][j] = new_board.__tiles[i + 1][j]
                new_board.__tiles[i + 1][j] = temp
                matches: list = new_board.check_matches()
                if len(matches) > 0:
                    return False

        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH - 1):
                new_board: MatchThreeBoard = self.clone()
                temp: MatchThreeTile = new_board.__tiles[i][j]
                new_board.__tiles[i][j] = new_board.__tiles[i][j + 1]
                new_board.__tiles[i][j + 1] = temp
                matches: list = new_board.check_matches()
                if len(matches) > 0:
                    return False

        return True

    def check_matches(self):
        # type: () -> list
        self.__matches = []  # initial value
        for j in range(self.BOARD_WIDTH):
            curr_match: list = []  # initial value
            for i in range(self.BOARD_HEIGHT):
                if len(curr_match) == 0 or self.__tiles[i][j].contents == self.__tiles[i - 1][j].contents:
                    curr_match.append((i, j))
                else:
                    if len(curr_match) >= 3:
                        self.__matches.append(curr_match)
                    curr_match = [(i, j)]
            if len(curr_match) >= 3:
                self.__matches.append(curr_match)

        for i in range(self.BOARD_HEIGHT):
            curr_match: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                if len(curr_match) == 0 or self.__tiles[i][j].contents == self.__tiles[i][j - 1].contents:
                    curr_match.append((i, j))
                else:
                    if len(curr_match) >= 3:
                        self.__matches.append(curr_match)
                    curr_match = [(i, j)]
            if len(curr_match) >= 3:
                self.__matches.append(curr_match)

        return self.__matches

    def clear_matches(self):
        # type: () -> None
        for match in self.__matches:
            for position in match:
                self.__tiles[position[0]][position[1]].contents = "NONE"

        self.__matches = []

    def fill_board(self):
        # type: () -> None
        for j in range(self.BOARD_WIDTH):
            for i in range(self.BOARD_HEIGHT):
                if self.__tiles[i][j].contents == "NONE":
                    for row in range(i, 0, -1):
                        self.__tiles[row][j].contents = self.__tiles[row - 1][j].contents
                    self.__tiles[0][j].contents = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                                  len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]
                    while self.__tiles[0][j].contents == self.__tiles[1][j].contents or (j > 0 and
                                                                                         self.__tiles[0][j].contents ==
                                                                                         self.__tiles[0][
                                                                                             j - 1].contents) or \
                            (j < self.BOARD_WIDTH - 1 and self.__tiles[0][j].contents == self.__tiles[0][
                                j + 1].contents):
                        self.__tiles[0][j].contents = MatchThreeTile.POSSIBLE_KEYWORDS[random.randint(0,
                                                                                                      len(MatchThreeTile.POSSIBLE_KEYWORDS) - 1)]

    def get_tile_at(self, x, y):
        # type: (int, int) -> MatchThreeTile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def get_tiles(self):
        # type: () -> list
        return self.__tiles

    def __str__(self):
        # type: () -> str
        return str(tabulate(self.__tiles, tablefmt='fancy_grid'))

    def clone(self):
        # type: () -> MatchThreeBoard
        return copy.deepcopy(self)


class MatchThreeTile:
    """
    This class contains attributes of a tile in the minigame "Match-3 Game".
    """

    POSSIBLE_KEYWORDS: list = ["AND", "AS", "ASSERT", "BREAK", "CLASS", "CONTINUE", "DEF", "DEL", "ELIF", "ELSE",
                               "EXCEPT", "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL"]

    def __init__(self, contents):
        # type: (str) -> None
        self.contents: str = contents if contents in self.POSSIBLE_KEYWORDS else "NONE"

    def __str__(self):
        # type: () -> str
        return str(self.contents)

    def clone(self):
        # type: () -> MatchThreeTile
        return copy.deepcopy(self)


###########################################
# MATCH-3 GAME
###########################################


###########################################
# ADVENTURE MODE
###########################################


class Action:
    """
    This class contains attributes of an action that can take place during battles.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in self.POSSIBLE_NAMES else self.POSSIBLE_NAMES[0]

    def __str__(self):
        # type: () -> str
        res: str = str(type(self).__name__) + "("  # initial value
        index: int = 0  # initial value
        for item in vars(self).items():
            res += str(item[0]) + "=" + str(item[1])

            if index < len(vars(self).items()) - 1:
                res += ", "

            index += 1

        return res + ")"

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class AwakenBonus:
    """
    This class contains attributes of the bonus gained for awakening a legendary creature.
    """


class Battle:
    """
    This class contains attributes of a battle in this game.
    """


class PVPBattle(Battle):
    """
    This class contains attributes of a battle between players.
    """


class WildBattle(Battle):
    """
    This class contains attributes of a battle against a legendary creature.
    """


class TrainerBattle(Battle):
    """
    This class contains attributes of a battle between legendary creature trainers.
    """


class Planet:
    """
    This class contains attributes of the planet in this game.
    """


class City:
    """
    This class contains attributes of a city in this game.
    """


class CityTile:
    """
    This class contains attributes of a tile in a city.
    """


class Portal:
    """
    This class contains attributes of a portal from one city to another.
    """


class WallTile(CityTile):
    """
    This class contains attributes of a city tile with a wall where the player cannot be at.
    """


class WaterTile(CityTile):
    """
    This class contains attributes of a city tile of a body of water where the player cannot be at.
    """


class GrassTile(CityTile):
    """
    This class contains attributes of a city tile with grass where the player can encounter wild legendary creatures.
    """


class PavementTile(CityTile):
    """
    This class contains attributes of a tile with pavement where the player can walk safely without any distractions
    from wild legendary creatures.
    """


class Building:
    """
    This class contains attributes of a building in a city.
    """


class ItemShop(Building):
    """
    This class contains attributes of an item shop to buy items in the adventure mode.
    """


class FusionCenter(Building):
    """
    This class contains attributes of a fusion center used to fuse legendary creatures.
    """


class BattleGym(Building):
    """
    This class contains attributes of a battle gym where CPU controlled trainers are available for the player to battle
    against.
    """


class Dungeon(Building):
    """
    This class contains attributes of an adventure mode dungeon where wild legendary creatures and CPU controlled
    trainers are available for the player to battle against.
    """


class Daycare(Building):
    """
    This class contains attributes of a daycare used to place legendary creatures to be trained automatically. In this
    case, the legendary creature being placed will automatically gain EXP.
    """


class Floor:
    """
    This class contains attributes of a floor in a building.
    """


class FloorTile:
    """
    This class contains attributes of a tile in a building floor.
    """


class NormalFloorTile(FloorTile):
    """
    This class contains attributes of a normal floor tile.
    """


class WildFloorTile(FloorTile):
    """
    This class contains attributes of a floor tile where wild legendary creatures can be encountered.
    """


class BuildingEntryOrExit(FloorTile):
    """
    This class contains attributes of a tile used to enter or exit a building.
    """


class StaircaseTile(FloorTile):
    """
    This class contains attributes of a staircase tile for the player to go upstairs/downstairs.
    """


###########################################
# ADVENTURE MODE
###########################################


###########################################
# INVENTORY
###########################################


class LegendaryCreatureInventory:
    """
    This class contains attributes of an inventory containing legendary creatures.
    """


class ItemInventory:
    """
    This class contains attributes of an inventory containing items.
    """


###########################################
# INVENTORY
###########################################


###########################################
# LEGENDARY CREATURE
###########################################


class BattleTeam:
    """
    This class contains attributes of a team brought to battles.
    """


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in this game.
    """


class Skill:
    """
    This class contains attributes of a skill legendary creatures have.
    """


class ActiveSkill(Skill):
    """
    This class contains attributes of an active skill legendary creatures have.
    """


class PassiveSkill(Skill):
    """
    This class contains attributes of a passive skill legendary creatures have.
    """


class PassiveSkillEffect:
    """
    This class contains attributes of the effect of a passive skill.
    """


class LeaderSkill(Skill):
    """
    This class contains attributes of a leader skill legendary creatures have.
    """


class LeaderSkillEffect:
    """
    This class contains attributes of the effect of a leader skill.
    """


class DamageMultiplier:
    """
    This class contains attributes of the damage multiplier of a skill.
    """


class BeneficialEffect:
    """
    This class contains attributes of a beneficial effect a legendary creature has.
    """


class HarmfulEffect:
    """
    This class contains attributes of a harmful effect a legendary creature has.
    """


###########################################
# LEGENDARY CREATURE
###########################################


###########################################
# ITEMS
###########################################


class Item:
    """
    This class contains attributes of an item in this game.
    """


class TrainerItem(Item):
    """
    This class contains attributes of an item to be used by trainers.
    """


class Weapon(TrainerItem):
    """
    This class contains attributes of a weapon the trainers can bring to PVP battles.
    """


class Armor(TrainerItem):
    """
    This class contains attributes of an armor the trainers can bring to PVP battles.
    """


class Crop(TrainerItem):
    """
    This class contains attributes of a crop the trainers can grow in this game.
    """


class LegendaryCreatureItem(Item):
    """
    This class contains attributes of an item to be used by legendary creatures.
    """


class Egg(LegendaryCreatureItem):
    """
    This class contains attributes of an egg which can be hatched to produce a new legendary creature
    """


class Ball(LegendaryCreatureItem):
    """
    This class contains attributes of a ball used to catch a legendary creature.
    """


class Rune(LegendaryCreatureItem):
    """
    This class contains attributes of a rune used to strengthen legendary creatures.
    """


class SetEffect:
    """
    This class contains attributes of a set effect of a rune.
    """


class StatIncrease:
    """
    This class contains attributes of the increase in stats of a rune.
    """


class AwakenShard(Item):
    """
    This class contains attributes of an awaken shard to immediately awaken a legendary creature.
    """


class EXPShard(Item):
    """
    This class contains attributes of an EXP shard to increase the EXP of a legendary creature.
    """


class LevelUpShard(Item):
    """
    This class contains attributes of a shard used to immediately level up a legendary creature.
    """


class SkillLevelUpShard(Item):
    """
    This class contains attributes of a skill level up shard to immediately increase the level of a
    skill possessed by a legendary creature.
    """


###########################################
# ITEMS
###########################################


###########################################
# EXERCISE
###########################################


class ExerciseGym:
    """
    This class contains attributes of a gym where the player can improve his/her attributes.
    """


class FitnessType:
    """
    This class contains attributes of the type of fitness in an exercise gym.
    """


class TrainingOption:
    """
    This class contains attributes of a training option for fitness.
    """


###########################################
# EXERCISE
###########################################


###########################################
# PROPERTIES
###########################################


class Property:
    """
    This class contains attributes of a property the player can live in.
    """


class PropertyUpgrade:
    """
    This class contains attributes of an upgrade to a property a player owns.
    """


###########################################
# PROPERTIES
###########################################


###########################################
# JOBS AND SKILLS
###########################################


class JobRole:
    """
    This class contains attributes of a job role a player can get in this game.
    """


class Course:
    """
    This class contains attributes of a course the player can take in this game.
    """


###########################################
# JOBS AND SKILLS
###########################################


###########################################
# PLANTATION
###########################################


class Plantation:
    """
    This class contains attributes of a player's plantation to grow crops.
    """


class Section:
    """
    This class contains attributes of a section in a plantation.
    """


class SectionTile:
    """
    This class contains attributes of a tile in a section.
    """


###########################################
# PLANTATION
###########################################


###########################################
# GENERAL
###########################################


class GameCharacter:
    """
    This class contains attributes of a game character in this game.
    """


class NPC(GameCharacter):
    """
    This class contains attributes of a non-player character (NPC).
    """


class Trainer(GameCharacter):
    """
    This class contains attributes of a trainer in this game.
    """


class PlayerTrainer(Trainer):
    """
    This class contains attributes of the player in this game.
    """


class CPUTrainer(Trainer):
    """
    This class contains attributes of a CPU controlled trainer.
    """


class AdventureModeLocation:
    """
    This class contains attributes of the location of a game character in adventure mode of this game.
    """


class Jail:
    """
    This class contains attributes of the jail.
    """


class Hospital:
    """
    This class contains attributes of the hospital for injured game characters.
    """


class AwardCondition:
    """
    This class contains attributes of a condition for an award to be achieved.
    """


class Award:
    """
    This class contains attributes of an award a player can get for achieving something.
    """


class ResourceReward:
    """
    This class contains attributes of the resources gained for doing something.
    """


class Game:
    """
    This class contains attributes of saved game data.
    """


###########################################
# GENERAL
###########################################


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    print("Welcome to 'Life Simulation' by 'SoftwareApkDev'.")
    print("This game is an offline adventure and simulation RPG allowing the player to ")
    print("choose various real-life actions.")
    print("Below is the element chart in 'Adventure Mode' of 'Life Simulation'.\n")
    print(str(tabulate_element_chart()) + "\n")
    print("The following elements do not have any elemental strengths nor weaknesses.")
    print("This is because they are ancient world elements. In this case, these elements will always ")
    print("be dealt with normal damage.\n")
    ancient_world_elements: list = ["BEAUTY", "MAGIC", "CHAOS", "HAPPY", "DREAM", "SOUL"]
    for i in range(0, len(ancient_world_elements)):
        print(str(i + 1) + ". " + str(ancient_world_elements[i]))

    return 0


if __name__ == '__main__':
    main()
