import random as rd
import pandas as pd

from .make_dataframes import EntityTables


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

# Different armour levels for characters
armour_levels = {
    '1': ['hide', 'leather'],
    '2': ['hide', 'leather', 'lamellar', 'gambeson'],
    '3': {
        'Light': ['leather', 'lamellar', 'gambeson'],
        'Heavy':  ['cuirass', 'ring', 'scale', 'laminar', 'maille']
    },
    '4': {
        'Light': ['lamellar', 'gambeson'],
        'Heavy':  ['maille', 'splint', 'plate']
    }
}


def convertDice(dice):
    dIndex = dice.index('d')

    nDice = int(dice[:dIndex])
    sDice = int(dice[dIndex + 1:])

    return nDice, sDice


def rollStat(number, dice, bonus):
    base = 0
    for _ in range(number):
        base += rd.randint(1, dice)
    stat = base + bonus

    return stat


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


class EntityStats:
    
    def __init__(self):
        self.tables = EntityTables(1)

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

        weapon.type = wepDict['Type']

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
        if wepDict['Heavy']:
            weapon.is_heavy = True
        if wepDict['Finesse']:
            weapon.is_finesse = True

        if wepDict['Protection']:
            weapon.protection = wepDict['Protection']
            weapon.defense_type = wepDict['Defense Type']

    def getArmourStats(self, armour):
        arDict = self.getArmourDict(armour.name)

        armour.type = arDict['Type']
        armour.value = int(arDict['Value'])
        armour.restriction = int(arDict['Dex Penalty'])
        armour.weight = int(arDict['Movement Penalty'])

    def getObjectStats(self, i_object):
        objDict = self.getArmourDict(i_object.name)

        i_object.armour['pierce'] = int(objDict['AC'])
        i_object.armour['slash'] = int(objDict['AC'])
        i_object.armour['bludgeon'] = int(objDict['AC'])
        i_object.baseHealth = int(objDict['Health'])

        is_inv = bool(objDict['Inventory'])

        if is_inv:
            i_object.inventory = []

    # Adds the stats to the given character (not player)
    def getCharacterStats(self, character):  # Doesn't collect all data
        characterName = character.name
        charDict = self.getCharacterDict(characterName)
        
        size = charDict['Size']

        if charDict['Base Damage']:
            character.baseDamage = convertDice(charDict['Base Damage'])
        if charDict['Base Armour']:
            character.baseArmour = charDict['Base Armour']
        if charDict['Inventory']:
            character.inventory = convertList(charDict['Inventory'])

        if charDict['Armour Level']:
            level = charDict['Armour Level']

            if int(level) < 3:
                for armour_type in armour_levels[level]:
                    armour_list = armour_levels[level][armour_type]
                    character.armour[armour_type] = rd.choice(armour_list)
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
        character.hitProf = int(charDict['Experience'])
        character.baseMovement = int(charDict['Speed'])
        character.drop_rate = int(charDict['Drop Rate'])
        
        character.baseStat['STR'] = int(charDict['STR'])
        character.baseStat['DEX'] = int(charDict['DEX'])
        character.baseStat['CON'] = int(charDict['CON'])
        character.baseStat['WIT'] = int(charDict['WIT'])
        
        character.baseHealth = rollStat(character.hitProf, character.baseStat['CON'], character.baseStat['CON'])
        if size == 'large':
            character.baseSize = 10
        elif size == 'huge':
            character.baseSize = 15
        elif size == 'gargantuan':
            character.baseSize = 20
        else:
            character.baseSize = 5

        character.baseReach = character.baseSize

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
    
