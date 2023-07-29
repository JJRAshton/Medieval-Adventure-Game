from typing import List, Tuple
import random as rd

def convertDice(dice: str) -> Tuple[int, int]:
    dIndex = dice.index('d')

    nDice = int(dice[:dIndex])
    sDice = int(dice[dIndex + 1:])

    return nDice, sDice


def rollStat(number: int, dice: int, bonus: int):
    base = 0
    for _ in range(number):
        base += rd.randint(1, dice)
    stat = base + bonus

    return stat


def convertList(list_str: str):
    no_whitespace = list_str.replace(" ", "")
    if no_whitespace == "":
        return []
    return no_whitespace.split(",")
