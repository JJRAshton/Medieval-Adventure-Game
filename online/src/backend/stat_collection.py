import create_stat_tables as cst


def convertDice(dice):
    dIndex = dice.index('d')

    nDice = int(dice[:dIndex])
    sDice = int(dice[dIndex + 1:])

    return nDice, sDice


class Stats:
    
    def __init__(self):
        self.characterTable, self.weaponTable = cst.make_stat_tables()
    
    def getWeaponDict(self, weaponName):
        weaponDict = cst.get_weapon_stats_dict(weaponName, self.weaponTable)
        return weaponDict
    
    def getCharacterDict(self, characterName):
        characterDict = cst.get_character_stats_dict(characterName, self.characterTable)
        return characterDict
        
    def getWeaponStats(self, weapon):   # Doesn't collect all data
        wepDict = self.getWeaponDict(weapon.name)
        
        damageStr = wepDict['Damage']
        
        weapon.reach = int(wepDict['Range'])
        weapon.damage = convertDice(damageStr)

    def getCharacterStats(self, character):  # Doesn't collect all data
        characterName = character.name
        charDict = self.getCharacterDict(characterName)
        
        size = charDict['Size']
        character.primaryWeapon = charDict['Weapon']
        
        character.profBonus = int(charDict['Proficiency Bonus'])
        character.maxHealth = int(charDict['Health'])
        character.armourClass = int(charDict['AC'])
        character.maxMovement = int(charDict['Speed'])
        
        character.baseStat['STR'] = int(charDict['STR'])
        character.baseStat['DEX'] = int(charDict['DEX'])
        
        if size == 'small':
            character.baseSize = 5
        elif size == 'medium':
            character.baseSize = 5
        elif size == 'large':
            character.baseSize = 10
        elif size == 'huge':
            character.baseSize = 15
            
    def getPlayerStats(self, player):   # Doesn't collect all data
        charDict = self.getPlayerDict(playerName)   # Needs to pick random stat
        
        size = charDict['Size']
        player.primaryWeapon = charDict['Weapon']
        
        player.profBonus = int(charDict['Proficiency Bonus'])
        player.maxHealth = int(charDict['Health'])
        player.armourClass = int(charDict['AC'])
        player.maxMovement = int(charDict['Speed'])
        
        player.baseStat['STR'] = int(charDict['STR'])
        player.baseStat['DEX'] = int(charDict['DEX'])
        
        if size == 'small':
            player.baseSize = 5
        elif size == 'medium':
            player.baseSize = 5
        elif size == 'large':
            player.baseSize = 10
        elif size == 'huge':
            player.baseSize = 15
    
