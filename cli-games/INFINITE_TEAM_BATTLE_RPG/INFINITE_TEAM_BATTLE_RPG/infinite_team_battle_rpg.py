"""
This file contains code for the game "Infinite Team Battle RPG".
Author: SoftwareApkDev
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


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


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
# BATTLE
###########################################


class Action:
    """
    This class contains attributes of an action that can be carried out during battles.
    """


class Battle:
    """
    This class contains attributes of a battle that can take place.
    """


###########################################
# BATTLE
###########################################


###########################################
# LEGENDARY CREATURE
###########################################


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in this game.
    """


###########################################
# LEGENDARY CREATURE
###########################################


###########################################
# ITEM
###########################################


class Item:
    """
    This class contains attributes of an item in this game.
    """


###########################################
# ITEM
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
# GENERAL
###########################################


class ItemShop:
    """
    This class contains attributes of a shop selling items.
    """


class Player:
    """
    This class contains attributes of the player in this game.
    """


class ResourceReward:
    """
    This class contains attributes of the resources gained as a reward for doing something in this game.
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


if __name__ == '__main__':
    main()
