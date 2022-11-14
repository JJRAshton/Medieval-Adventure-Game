from .tables import Tables
import random as rd


def convertDice(dice):
    dIndex = dice.index('d')

    nDice = int(dice[:dIndex])
    sDice = int(dice[dIndex + 1:])

    return nDice, sDice


def convertDiceEx(dice):
    dIndex = dice.index('d')
    plusIndex = dice.index('+')

    nDice = int(dice[:dIndex])
    sDice = int(dice[dIndex + 1:plusIndex-1])
    bonus = int(dice[plusIndex + 2:])

    return nDice, sDice, bonus


def convertList(str):
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

    # Returns a dictionary of stats for the given player
    def getPlayerDict(self, number):
        playerDict = self.tables.get_player_stats_dict(number)
        return playerDict

    # Adds the stats to the given weapon
    def getWeaponStats(self, weapon):   # Doesn't collect all data
        wepDict = self.getWeaponDict(weapon.name)
        
        damageStr = wepDict['Damage']
        
        weapon.reach = int(wepDict['Range'])
        weapon.damage = convertDice(damageStr)

    def getArmourStats(self, armour):
        arDict = self.getArmourDict(armour.name)

        armour.type = arDict['Type']
        armour.armourValue = int(arDict['Value'])

    def getObjectStats(self, i_object):
        objDict = self.getArmourDict(i_object.name)

        i_object.armourClass = int(objDict['AC'])
        i_object.baseHealth = int(objDict['Health'])

        is_inv = bool(objDict['Inventory'])

        if is_inv:
            i_object.inventory = []

    # Adds the stats to the given character (not player)
    def getCharacterStats(self, character):  # Doesn't collect all data
        characterName = character.name
        charDict = self.getCharacterDict(characterName)
        
        size = charDict['Size']
        if charDict['Weapon'] != '':
            character.primaryWeapon = charDict['Weapon']
        if charDict['Base Damage'] != '':
            character.baseDamage = convertDice(charDict['Base Damage'])
        if charDict['Armour'] != '':
            character.armour = charDict['Armour']
        if charDict['Base Armour'] != '':
            character.baseArmour = charDict['Base Armour']

        number, dice, bonus = convertDiceEx(charDict['Health'])
        base = 0
        for _ in range(number):
            base += rd.randint(1, dice)
        character.baseHealth = base + bonus

        if charDict['Inventory'] != '':
            character.inventory = convertList(charDict['Inventory'])

        character.profBonus = int(charDict['Proficiency Bonus'])
        character.maxMovement = int(charDict['Speed'])
        character.drop_rate = int(charDict['Drop Rate'])
        
        character.baseStat['STR'] = int(charDict['STR'])
        character.baseStat['DEX'] = int(charDict['DEX'])
        character.baseStat['CON'] = int(charDict['CON'])
        character.baseStat['INT'] = int(charDict['INT'])
        character.baseStat['WIS'] = int(charDict['WIS'])
        character.baseStat['CHA'] = int(charDict['CHA'])
        
        if size == 'small':
            character.baseSize = 5
        elif size == 'medium':
            character.baseSize = 5
        elif size == 'large':
            character.baseSize = 10
        elif size == 'huge':
            character.baseSize = 15

    # Adds the stats to the given player
    def getPlayerStats(self, player):   # Doesn't collect all data
        statNumber = str(rd.randint(1, 10))
        statNumber = 1
        charDict = self.getPlayerDict(statNumber)   # Needs to pick random stat
        
        size = charDict['Size']
        player.primaryWeapon = charDict['Weapon']
        player.armour = charDict['Armour']
        player.type = charDict['Class']

        player.lvl = int(charDict['Level'])
        player.maxMovement = int(charDict['Speed'])
        
        player.baseStat['STR'] = int(charDict['STR'])
        player.baseStat['DEX'] = int(charDict['DEX'])
        player.baseStat['CON'] = int(charDict['CON'])
        player.baseStat['INT'] = int(charDict['INT'])
        player.baseStat['WIS'] = int(charDict['WIS'])
        player.baseStat['CHA'] = int(charDict['CHA'])

        
        if size == 'small':
            player.baseSize = 5
        elif size == 'medium':
            player.baseSize = 5
        elif size == 'large':
            player.baseSize = 10
        elif size == 'huge':
            player.baseSize = 15
    