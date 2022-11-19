import random as rd
import pandas as pd

from .assign_entity import convertList, convertDice, rollStat
from .make_dataframes import AttackTables


weapon_type_wep_atk = {
    'axes': 'hack',
    'bludgeons': ['bludgeon'],
    'bows': ['arrow'],
    'crossbows': ['bolt'],
    'double_edged_swords': ['cut', 'thrust'],
    'mythical': 'magic',
    'pierces': 'pierce',
    'single_edged_swords': 'slash',
    'slashes': 'slash',
    'special': 'magic',
    'staves': 'magic',
    'throwables': 'pierce',
    'wands': 'magic'
}


weapon_type_raw_atk = {
    'axes': 'hack',
    'bludgeons': ['bludgeon'],
    'bows': ['arrow'],
    'crossbows': ['bolt'],
    'double_edged_swords': ['cut', 'thrust', ''],
    'mythical': 'magic',
    'pierces': 'pierce',
    'single_edged_swords': 'slash',
    'slashes': 'slash',
    'special': 'magic',
    'staves': 'magic',
    'throwables': 'pierce',
    'wands': 'magic'
}


class AttackStats:

    def __init__(self):

        self.tables = AttackTables()

    # Returns a dictionary of stats for the given attack
    def getWeaponAttackDict(self, attackName):
        attackDict = self.tables.get_weapon_attack_stats_dict(attackName)
        return attackDict

    # Returns a dictionary of stats for the given attack
    def getRawAttackDict(self, attackName):
        attackDict = self.tables.get_raw_attack_stats_dict(attackName)
        return attackDict

    def getWeaponAttackStats(self, attack):
        atkDict = self.getWeaponAttackDict(attack.name)

        attack.type = atkDict['Type']
        attack.value = int(atkDict['Value'])

    def getRawAttackStats(self, attack):
        atkDict = self.getRawAttackDict(attack.name)

        attack.type = atkDict['Type']
        attack.value = int(atkDict['Value'])