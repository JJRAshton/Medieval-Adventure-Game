
"""Keeps Track of All Creature Stats"""

stats = {}
sizeDict = {'small':6, 'medium':8, 'large':10, 'huge':12, 'gargantuan':20}
def addCreature(creatureDict, creatureName, stats = stats):
    stats[creatureName] = {}
    for stat in creatureDict:
        stats[creatureName][stat] = creatureDict[stat]
    
    return stats
    
def createCreature(creatureName, CON, DEX, Size, n):
    global stats
    global sizeDict
    
    creatureDict = {}
    
    creatureDict['CON'] = CON
    creatureDict['DEX'] = DEX
    
    creatureDict['Size'] = Size
    
    creatureDict['n_Hit_Dice'] = n
    creatureDict['Hit_Dice'] = [creatureDict['n_Hit_Dice'], sizeDict[creatureDict['Size']]]
    
    stats = addCreature(creatureDict, creatureName, stats)
    
createCreature('orc', 1, 2, 'medium', 2)
createCreature('Elrond', 1, 2, 'medium', 5)
createCreature('troll', 4, -1, 'large', 10)
createCreature('dwarf', 3, 0, 'medium', 4)