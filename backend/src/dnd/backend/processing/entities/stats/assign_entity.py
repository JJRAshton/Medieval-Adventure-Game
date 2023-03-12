import random as rd
from typing import List
import pandas as pd

from ..entity import HealthEntity
from ..item import Weapon
from ..item import Armour

from .make_dataframes import EntityTables


# Different armour levels for characters
armour_levels = {
    1: ['hide', 'leather'],
    2: ['hide', 'leather', 'padded_tunic', 'arming_doublet', 'gambeson'],
    3: {
        'Under': ['hide', 'leather'],
        'Over': ['hauberk', 'scale', 'splint', 'lamellar']
    },
    4: {
        'Under': ['leather', 'padded_tunic', 'arming_doublet', 'gambeson', 'padded_jack'],
        'Over':  ['breastplate', 'cuirass', 'hauberk', 'hauberk_riveted', 'scale', 'splint', 'lamellar']
    },
    5: {
        'Under': ['padded_tunic', 'arming_doublet'],
        'Over':  ['laminar', 'plate', 'full_plate']
    }
}


def convertDice(dice: str):
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


class EntityStats:
    
    def __init__(self, mapNumber: int=1):
        self.tables = EntityTables(mapNumber)

    # Returns a dictionary of stats for the given weapon
    def getWeaponDict(self, weaponName: str):
        weaponDict = self.tables.get_weapon_stats_dict(weaponName)
        return weaponDict

    # Returns a dictionary of stats for the given character
    def getCharacterDict(self, characterName: str):
        characterDict = self.tables.get_character_stats_dict(characterName)
        return characterDict

    # Returns a dictionary of stats for the given armour
    def getArmourDict(self, armourName: str):
        armourDict = self.tables.get_armour_stats_dict(armourName)
        return armourDict

    # Adds the stats to the given weapon
    def getWeaponStats(self, weapon: Weapon):   # Doesn't collect all data
        wepDict = self.getWeaponDict(weapon.name)

        weapon.type = wepDict['Type']
        weapon.range = int(wepDict['Range'])
        if wepDict['Damage Dice']:
            weapon.damage_dice = int(wepDict['Damage Dice'][1:])

        weapon.attacks = convertList(wepDict['Attacks'])

        if wepDict['Ranged']:
            weapon.is_ranged = True
        if wepDict['Loading']:
            weapon.is_loading = True
        if wepDict['Two-handed']:
            weapon.is_twoHanded = True
        if wepDict['Arrows']:
            weapon.is_arrows = True
        if wepDict['Bolts']:
            weapon.is_bolts = True
        if wepDict['Light']:
            weapon.is_light = True
        if wepDict['Finesse']:
            weapon.is_finesse = True
        if wepDict['Armour Piercing']:
            weapon.is_AP = True
        if wepDict['Fine']:
            weapon.is_fine = True
        if wepDict['Magic']:
            weapon.is_magic = True
        if wepDict['Melee']:
            weapon.is_melee = False

        if wepDict['Protection']:
            weapon.protection = int(wepDict['Protection'])
            weapon.defense_type = wepDict['Defense Type']

    def getArmourStats(self, armour: Armour):
        arDict = self.getArmourDict(armour.name)

        armour.type = arDict['Type']
        armour.material = arDict['Material']
        armour.bulk = int(arDict['Bulk'])
        armour.coverage = int(arDict['Coverage'])
        armour.value = int(arDict['Armour Value'])
        armour.flex = int(arDict['Flex']) / 100
        armour.weight = int(arDict['Movement Penalty'])

    def getObjectStats(self, i_object):
        objDict = self.getArmourDict(i_object.name)

        i_object.armour['piercing'] = int(objDict['AC'])
        i_object.armour['slashing'] = int(objDict['AC'])
        i_object.armour['bludgeoning'] = int(objDict['AC'])
        i_object.baseHealth = int(objDict['Health'])

        is_inv = bool(objDict['Inventory'])

        if is_inv:
            i_object.inventory = []

    # Adds the stats to the given character (not player)
    def getCharacterStats(self, character: HealthEntity):  # Doesn't collect all data
        characterName = character.name
        charDict = self.getCharacterDict(characterName)
        startingItems: List[object] = []

        size = charDict['Size']

        for location in ['Left', 'Right', 'Both']:
            if charDict[location]:
                character.equippedWeapons[location] = charDict[location]
                startingItems.append(charDict[location])

        if charDict['Base Armour']:
            character.baseArmour = charDict['Base Armour']
            character.baseCoverage = 1
        if charDict['Inventory']:
            inventory = convertList(charDict['Inventory'])
            character.inventory = inventory
            startingItems += inventory
        if charDict['Skill']:
            character.skill = int(charDict['Skill'])

        character.base_attacks = convertList(charDict['Attacks'])

        character.starting_items = startingItems

        # Randomly selects armour according to armour level
        if charDict['Armour Level']:
            level = int(charDict['Armour Level'])

            if level > 2:
                for armour_type in armour_levels[level]:
                    armour_list = armour_levels[level][armour_type]
                    armour = rd.choice(armour_list)
                    character.armour[armour_type] = armour
                    if armour == 'padded_jack':
                        break
            else:
                armour_list = armour_levels[level]
                character.armour['Light'] = rd.choice(armour_list)

        if charDict['Vulnerabilities']:
            vulnerabilities = convertList(charDict['Vulnerabilities'])
            character.vulnerabilities += vulnerabilities
        if charDict['Resistances']:
            resistances = convertList(charDict['Resistances'])
            character.resistances += resistances

        character.actionsTotal = int(charDict['Actions'])
        character.baseMovement = int(charDict['Speed'])
        character.drop_rate = int(charDict['Drop Rate'])
        character.skill = int(charDict['Skill']) if charDict['Skill'] else 0
        character.difficulty = int(charDict['Difficulty'])

        character.baseStat['STR'] = int(charDict['STR'])
        character.baseStat['DEX'] = int(charDict['DEX'])
        character.baseStat['CON'] = int(charDict['CON'])
        character.baseStat['WIT'] = int(charDict['WIT'])

        character.baseEvasion = character.baseStat['DEX']
        
        character.baseHealth = rollStat(int(charDict['Difficulty']), character.baseStat['CON'], character.baseStat['CON'])
        if size == 'large':
            character.baseSize = 10
            character.dmg_mult = 2
        elif size == 'huge':
            character.baseSize = 15
            character.dmg_mult = 4
        elif size == 'gargantuan':
            character.baseSize = 20
            character.dmg_mult = 8
        else:
            character.baseSize = 5
            character.dmg_mult = 1

        character.baseReach = character.baseSize

    # Adds the stats to the given player
    def getPlayerStats(self, player):
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
        stat_rolls.sort(reverse=True)

        for stat in player.p_class.stat_order:
            player.baseStat[stat] = stat_rolls.pop(0)

        df = self.tables.weapons
        wep_option_df = pd.DataFrame()
        for wep_type in player.p_class.weapons:
            wepData = df[(df.Type == wep_type) & (df.Tier == 4)]
            wep_option_df = pd.concat([wep_option_df, wepData]) 

        choices = wep_option_df.index.tolist()
        weapon_str = rd.choice(choices)
        if df.loc[weapon_str].to_dict()['Two-handed']:
            player.equippedWeapons['Both'] = rd.choice(choices)
        else:
            player.equippedWeapons['Right'] = rd.choice(choices)
    
