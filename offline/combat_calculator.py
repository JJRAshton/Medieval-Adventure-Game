import random as rdm
import math as mt
import monster_stats as ms
"""Keeps Track of Creature Healths and Initiative Order in Combat"""

def roll(n, d):
    total = 0
    for i in range(n):
        total += int(rdm.random()*d)+1
    return total
        
class Creature:
    def __init__(self, ctype, team = 'opponent', colour = None, healthTemp=0):
        self.team = team
        self.init = 0
        self.ctype = ctype
        
        if ctype != 'player':
            self.colour = colour
            
            n, d = ms.stats[ctype]['Hit_Dice']
            b = n*ms.stats[ctype]['CON']
            self.hp = roll(n, d)+b
            self.tempHP = healthTemp
            self.prevhp = self.hp
            
            self.DEX = ms.stats[ctype]['DEX']
        
    #Updates the health of a creature
    def updateHealth(self, damage, tempHP=0):
        self.prevhp = self.hp
        self.tempHP += tempHP
        if damage >= self.tempHP:
            damage -= self.tempHP
            self.tempHP = 0
            self.hp -= damage
        else:
            self.tempHP -= damage
            
    #Reverts health back to previous in case of mistake
    def revertHealth(self):
        self.hp = self.prevhp
      
def createCreatureGroups(ctype, nCreatures, nGroups, team):
    
    #Magnet Colours
    colours = ['red', 'blue', 'yellow', 'orange', 'green']
    
    sizeGroups = [round(nCreatures/nGroups) for _ in range(nGroups-1)] + [nCreatures - (nGroups-1)*round(nCreatures/nGroups)]
    groups = {}
       
    if nGroups == 1:
        group = []
        creature = Creature(ctype, team)
        group.append(creature)
        groups[ctype] = group
    else:
        for n in range(nGroups):
            group = []
            for c in range(sizeGroups[n]):
                creature = Creature(ctype, team, colours[c])
                group.append(creature)
            groups[ctype+str(n+1)] = group
    
    return groups
    
#Outputs the initiative order of the creatures
def initiativeOrder(creatureGroups, rolls):
    
    groupList = []
    for creatureGroup in creatureGroups:
        groupList.append(creatureGroup)
        
    #Checks that the number of creatures and creature rolls is equal
    if len(groupList) != len(rolls):
        print('Invalid Number of Creature Rolls')
        return
    
    creatureRolls = list(zip(groupList, rolls))
    creatureRolls.sort(reverse=True)
    
    initOrder = [x[0] for x in creatureRolls]
    
    return initOrder

#Looks for repeated rolls now with players included
def checkRepeats(creatureGroups, rolls):
    
    for r1, group1 in enumerate(creatureGroups):
        for r2, group2 in enumerate(creatureGroups):
            if r1 == r2 or creatureGroups[group1][0].ctype != 'player' or creatureGroups[group2][0].ctype == 'player':
                continue
            if rolls[r1] == rolls[r2]:
                if creatureGroups[group2][0].team == 'opponent':
                    roll2 = 0
                    roll1 = 0
                    while roll1 == roll2:
                        print(group1+' has the same roll as '+group2) #Change to Interface
                        
                        roll1 = int(input(group1+' roll: ')) #Change to Interface
                        roll2 = roll(1, 20)+creatureGroups[group2][0].DEX
                else:
                    print(group1+' has the same roll as '+group2) #Change to Interface
                    roll2 = 10
                    x = int(input('x: ')) #Change to Interface
                    roll1 = roll2 + x
                if roll1 > roll2:
                    rolls[r1] += 0.2
                else:
                    rolls[r2] += 0.2
    
    return creatureGroups, rolls

#Rolls for creatures and checks for their repeats
def rollCreatures(creatureSpec):
    
    #Storage of all creature stats
    creatureGroups = {}
    #Adds creatures to creatureGroup dictionary
    for creature in creatureSpec:
        creat, number, numberG, team = creatureSpec[creature]
        groups = createCreatureGroups(creat, number, numberG, team)
        for group in groups:
            creatureGroups[group] = groups[group]
        
    #Rolls initiative for creatures
    rolls = []
    for group in creatureGroups:
        rolls.append(roll(1, 20)+creatureGroups[group][0].DEX)
        
    #Rerolls repeated creature rolls
    for r1, group1 in enumerate(creatureGroups):
        for r2, group2 in enumerate(creatureGroups):
            if r1 == r2:
                continue
            if rolls[r1] == rolls[r2]:
                roll1 = 0
                roll2 = 0
                while roll1 == roll2:
                    roll1 = roll(1, 20)+creatureGroups[group1][0].DEX
                    roll2 = roll(1, 20)+creatureGroups[group2][0].DEX
                if roll1 > roll2:
                    rolls[r1] += 0.1
                else:
                    rolls[r2] += 0.1
                    
    return creatureGroups, rolls

#Performs combat startup calculations
def createCombat(playersRoll, creatureSpec):

    creatureGroups, rolls = rollCreatures(creatureSpec)
    
    
    
    creatureGroups, rolls = checkRepeats(creatureGroups, rolls)
    
    initOrder = initiativeOrder(creatureGroups, rolls)
    
    return initOrder, creatureGroups, rolls

#Initiates combat
def startCombat(initOrder, creatureGroups, rolls):
    
    combatRound = 0
    while True:
        combatRound += 1
        for turn in range(len(initOrder)):
            x = input(initOrder[turn])