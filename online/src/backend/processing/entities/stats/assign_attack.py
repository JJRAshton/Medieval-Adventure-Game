import random as rd
import pandas as pd

from .assign_entity import convertDice
from .make_dataframes import AttackTables


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

    def getAttackStats(self, attack):
        if attack.name in self.tables.weapon_attacks.index.tolist():
            self.getWeaponAttackStats(attack)
        if attack.name in self.tables.raw_attacks.index.tolist():
            self.getRawAttackStats(attack)

    def getWeaponAttackStats(self, attack):
        atkDict = self.getWeaponAttackDict(attack.name)
        attack.type = 'weapon'

        dmg_type1 = atkDict['Dmg Typ 1']
        attack.damage_types[dmg_type1] = int(atkDict['Fraction 1'])
        attack.damage_maintype = dmg_type1
        if atkDict['Dmg Typ 2']:
            dmg_type2 = atkDict['Dmg Typ 2']
            attack.damage_types[dmg_type2] = 1 - int(atkDict['Fraction 1'])

        attack.damage = (int(atkDict['Dice No.']), 0)

    def getRawAttackStats(self, attack):
        atkDict = self.getRawAttackDict(attack.name)
        attack.type = 'raw'

        dmg_type1 = atkDict['Dmg Typ 1']
        attack.damage_types[dmg_type1] = int(atkDict['Fraction 1'])
        if atkDict['Dmg Typ 2']:
            dmg_type2 = atkDict['Dmg Typ 2']
            attack.damage_types[dmg_type2] = 1 - int(atkDict['Fraction 1'])

        attack.damage = convertDice(atkDict['Damage'])
