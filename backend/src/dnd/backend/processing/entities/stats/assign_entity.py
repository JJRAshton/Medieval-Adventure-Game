import random as rd
from typing import List
import pandas as pd

from ..item import Armour
from . import dice_utils

from .make_dataframes import EntityStatDictionaryProvider


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

''' Factory for armour, objects, characters and players. '''
class EntityFactory:

    def __init__(self, map_number: int=1):
        self.tables = EntityStatDictionaryProvider(map_number)

    # Returns a dictionary of stats for the given character
    def __getCharacterDict(self, character_name: str):
        character_dict = self.tables.get_character_stats_dict(character_name)
        return character_dict

    # Returns a dictionary of stats for the given armour
    def __getArmourDict(self, armour_name: str):
        armourDict = self.tables.get_armour_stats_dict(armour_name)
        return armourDict

    def getArmourStats(self, armour: Armour):
        arDict = self.__getArmourDict(armour.name)

        armour.type = arDict['Type']
        armour.material = arDict['Material']
        armour.bulk = int(arDict['Bulk'])
        armour.coverage = int(arDict['Coverage'])
        armour.value = int(arDict['Armour Value'])
        armour.flex = int(arDict['Flex']) / 100
        armour.weight = int(arDict['Movement Penalty'])

    def getObjectStats(self, i_object):
        obj_dict = self.__getArmourDict(i_object.name)

        i_object.armour['piercing'] = int(obj_dict['AC'])
        i_object.armour['slashing'] = int(obj_dict['AC'])
        i_object.armour['bludgeoning'] = int(obj_dict['AC'])
        i_object.baseHealth = int(obj_dict['Health'])

        is_inv = bool(obj_dict['Inventory'])

        if is_inv:
            i_object.inventory = []

    # Adds the stats to the given character (not player)
    def getCharacterStats(self, character):  # Doesn't collect all data
        character_name = character.name
        char_dict = self.__getCharacterDict(character_name)
        starting_items: List[object] = []

        size = char_dict['Size']

        for location in ['Left', 'Right', 'Both']:
            if char_dict[location]:
                character.equippedWeapons[location] = char_dict[location]
                starting_items.append(char_dict[location])

        if char_dict['Base Armour']:
            character.baseArmour = char_dict['Base Armour']
            character.baseCoverage = 1
        if char_dict['Inventory']:
            inventory = dice_utils.convertList(char_dict['Inventory'])
            character.inventory = inventory
            starting_items += inventory
        if char_dict['Skill']:
            character.skill = int(char_dict['Skill'])

        character.base_attacks = dice_utils.convertList(char_dict['Attacks'])

        character.starting_items = starting_items

        # Randomly selects armour according to armour level
        if char_dict['Armour Level']:
            level = int(char_dict['Armour Level'])

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

        if char_dict['Vulnerabilities']:
            vulnerabilities = dice_utils.convertList(char_dict['Vulnerabilities'])
            character.vulnerabilities += vulnerabilities
        if char_dict['Resistances']:
            resistances = dice_utils.convertList(char_dict['Resistances'])
            character.resistances += resistances

        character.actionsTotal = int(char_dict['Actions'])
        character.baseMovement = int(char_dict['Speed'])
        character.drop_rate = int(char_dict['Drop Rate'])
        character.skill = int(char_dict['Skill']) if char_dict['Skill'] else 0
        character.difficulty = int(char_dict['Difficulty'])

        character.baseStat['STR'] = int(char_dict['STR'])
        character.baseStat['DEX'] = int(char_dict['DEX'])
        character.baseStat['CON'] = int(char_dict['CON'])
        character.baseStat['WIT'] = int(char_dict['WIT'])

        character.baseEvasion = character.baseStat['DEX']
        
        character.baseHealth = dice_utils.rollStat(int(char_dict['Difficulty']), character.baseStat['CON'], character.baseStat['CON'])
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

        df = self.tables.__weapons
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
    
