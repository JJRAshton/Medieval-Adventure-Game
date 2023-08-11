from typing import Tuple
import random as rd


def convertDice(dice: str) -> Tuple[int, int]:
    n_dice, s_dice = dice.split('d')
    return int(n_dice), int(s_dice)


def roll_dice(number_of_dice: int, sides_per_dice: int, bonus: int = 0):
    return bonus + sum(rd.randint(1, sides_per_dice) for _ in range(number_of_dice))


def convertList(list_str: str):
    no_whitespace = list_str.replace(" ", "")
    if no_whitespace == "":
        return []
    return no_whitespace.split(",")

def safe_convert(list_str: str | None):
    if list_str:
        return convertList(list_str)
    return []

def roll_stats():
    x, n, top = 3, 8, 48  # roll 8, take best 5 - max of 40
    stat_rolls = []

    for _ in range(4):  # Number of stats to assign
        one_stat_roll = []
        for _ in range(n):  # Rolls n dice
            roll = rd.randint(1, int(top/x))
            one_stat_roll.append(roll)

        for _ in range(n-x):  # Get rid of the lowest values
            one_stat_roll.pop(one_stat_roll.index(min(one_stat_roll)))

        stat_rolls.append(sum(one_stat_roll))
    return stat_rolls