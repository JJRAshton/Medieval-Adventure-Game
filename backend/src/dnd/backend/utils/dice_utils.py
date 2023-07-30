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
