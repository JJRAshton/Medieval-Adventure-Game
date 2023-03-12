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
    while ' ' in list_str:
        index = list_str.index(' ')
        list_str = list_str[:index] + list_str[index + 1:]
    str_list: List[str] = []
    while ',' in list_str:
        c_index = list_str.index(',')
        item = list_str[:c_index]
        list_str = list_str[c_index + 1:]
        str_list.append(item)
    str_list.append(list_str)

    return str_list
