import random as rd
import pandas as pd

from .tables import Tables


# Order of stats for classes
class_stat_order = {
    'Beserker': ['STR', 'CON', 'DEX', 'WIT'],
    'Gladiator': ['CON', 'DEX', 'STR', 'WIT'],
    'Ranger': ['STR', 'WIT', 'DEX', 'CON'],
    'Knight': ['CON', 'STR', 'WIT', 'DEX'],
    'Archer': ['DEX', 'STR', 'WIT', 'CON'],
    'Professor': ['WIT', 'DEX', 'CON', 'STR'],
    'Samurai': ['DEX', 'WIT', 'STR', 'CON']
}


def convertDice(dice):
    dIndex = dice.index('d')

    nDice = int(dice[:dIndex])
    sDice = int(dice[dIndex + 1:])

    return nDice, sDice


def convertDiceEx(dice):
    dIndex = dice.index('d')
    nDice = int(dice[:dIndex])
    if '+' in dice:
        plusIndex = dice.index('+')

        sDice = int(dice[dIndex + 1:plusIndex-1])
        bonus = int(dice[plusIndex + 2:])
    else:
        sDice = int(dice[dIndex + 1:])
        bonus = 0

    return nDice, sDice, bonus


def convertList(str):
    while ' ' in str:
        index = str.index(' ')
        str = str[:index] + str[index + 1:]
    list = []
    while ',' in str:
        c_index = str.index(',')
        item = str[:c_index]
        str = str[c_index + 1:]
        list.append(item)
    list.append(str)

    return list



class Stats:
    
    def __init__(self):
        self.tables = Tables(1)

    # Returns a dictionary of stats for the given weapon
    def getWeaponDict(self, weaponName):
        weaponDict = self.tables.get_weapon_stats_dict(weaponName)
        return weaponDict

    # Returns a dictionary of stats for the given character
    def getCharacterDict(self, characterName):
        characterDict = self.tables.get_character_stats_dict(characterName)
        return characterDict

    # Returns a dictionary of stats for the given armour
    def getArmourDict(self, armourName):
        armourDict = self.tables.get_armour_stats_dict(armourName)
        return armourDict

    # Adds the stats to the given weapon
    def getWeaponStats(self, weapon):   # Doesn't collect all data
        wepDict = self.getWeaponDict(weapon.name)
        
        damageStr = wepDict['Damage']
        
        weapon.reach = int(wepDict['Range'])
        weapon.damage = convertDice(damageStr)

    def getArmourStats(self, armour):
        arDict = self.getArmourDict(armour.name)

        armour.type = arDict['Type']
        armour.value = int(arDict['Value'])
        armour.restriction = int(arDict['Dex Penalty'])
        armour.weight = int(arDict['Movement Penalty'])

    def getObjectStats(self, i_object):
        objDict = self.getArmourDict(i_object.name)

        i_object.armour = int(objDict['AC'])
        i_object.baseHealth = int(objDict['Health'])

        is_inv = bool(objDict['Inventory'])

        if is_inv:
            i_object.inventory = []

    # Adds the stats to the given character (not player)
    def getCharacterStats(self, character):  # Doesn't collect all data
        characterName = character.name
        charDict = self.getCharacterDict(characterName)
        
        size = charDict['Size']
        if not isinstance(charDict['Weapon'], float):
            character.equippedWeapons = charDict['Weapon']
        if not isinstance(charDict['Base Damage'], float):
            character.baseDamage = convertDice(charDict['Base Damage'])
        if not isinstance(charDict['Armour'], float):
            character.equippedArmour = charDict['Armour']
        if not isinstance(charDict['Base Armour'], float):
            character.baseArmour = charDict['Base Armour']

        if 'd' in charDict['Health']:
            number, dice, bonus = convertDiceEx(charDict['Health'])
            base = 0
            for _ in range(number):
                base += rd.randint(1, dice)
            character.baseHealth = base + bonus
        else:
            character.baseHealth = int(charDict['Health'])

        if not isinstance(charDict['Inventory'], float):
            character.inventory = convertList(charDict['Inventory'])

        character.attacksTotal = int(charDict['Attacks'])
        character.hitProf = int(charDict['Proficiency Bonus'])
        character.baseMovement = int(charDict['Speed'])
        character.drop_rate = int(charDict['Drop Rate'])
        
        character.baseStat['STR'] = int(charDict['STR'])
        character.baseStat['DEX'] = int(charDict['DEX'])
        character.baseStat['CON'] = int(charDict['CON'])
        character.baseStat['WIT'] = int(charDict['WIT'])
        
        if size == 'small':
            character.baseSize = 5
        elif size == 'medium':
            character.baseSize = 5
        elif size == 'large':
            character.baseSize = 10
        elif size == 'huge':
            character.baseSize = 15

    # Adds the stats to the given player
    def getPlayerStats(self, player):
        x, n, top = 5, 8, 40  # roll 8, take best 5 - max of 40
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

        for stat in class_stat_order[player.type]:
            player.baseStat[stat] = stat_rolls.pop(0)

        df = self.tables.weapons
        wep_option_df = pd.DataFrame()
        for wep_type in player.class_weapons[player.type]:
            wepData = df[(df.Type == wep_type) & (df.Tier == 0)]
            wep_option_df = pd.concat([wep_option_df, wepData])

        choices = wep_option_df.index.tolist()
        player.equippedWeapons['Right'] = rd.choice(choices)

        if player.type in ['Knight', 'Samurai']:
            player.equippedArmour['Light'] = 'Leather'

        class_dict = self.tables.get_class_stats_dict(player.type)
        player.baseMovement = int(class_dict['Base Movement'])
        player.baseEvasion = int(class_dict['Base Evasion'])
        player.baseArmour = int(class_dict['Base Armour'])
        player.healthIncrement = int(class_dict['Health Increment'])
    
