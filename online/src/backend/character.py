from objects import Entity
import random as rd

class AnimateEntity(Entity):
    def __init__(self, entityName, entityID):
        super().__init__(self, entityName, entityID)
        self.maxMovement = 0
        self.profBonus = 0
        
        self.baseStat = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'INT': 0,
            'WIS': 0,
            'CHAR': 0
            }
        
        self.actionsTotal = 1
        self.attacksTotal = 1
        self.reactionsTotal = 1
        self.bonusactionsTotal = 0

        self.actions = 1
        self.attacks = 1
        self.reactions = 1
        self.bonusactions = 0
        
        self.hitDiceValue = 0
        self.hitDiceNumber = 0
        
        self.primaryWeapon = None
        self.armour = None

        self.damage = (0,0)
        self.atkMod = 0
        self.reach = 0

        self.armourClass = 0
        
        self.movement = 0
        
        self.unconscious = False
        self.savingThrows = (0,0)
        
        self.resetStats()
        self.levelUp()
        self.refreshModifierStat()
        self.refreshArmourStat()
        self.refreshWeaponStat()
    
    #Moves entity by given vector and decreases movement
    def move(self, vector):
        super().move(vector)
        count = abs(vector[0])+abs(vector[1])
        self.movement -= 5*count
    
    #Makes an attack roll returning whether it 0:critical fail, 1:miss, 2:hit, 3:critical hit
    def attackRoll(self, armourClass):
        atkBonus = self.atkMod + self.profBonus
        roll = rd.randint(1,20)

        if roll == 1:
            result = 0
        elif roll == 20:
            result = 3
        elif roll+atkBonus < armourClass:
            result = 1
        elif roll+atkBonus > armourClass:
            result = 2

        return result

    #Performs an attack on another creature
    def attack(self, creature):
        rollResult = self.attackRoll(creature.armourClass)

        if rollResult > 1:
            if rollResult == 2:
                damage = self.damage
            elif rollResult == 3:
                damage = (2*self.damage[0], self.damage[1], self.damage[2])
            appliedDamage = creature.takeDamage(damage)
            indicator = str(appliedDamage)
        else:
            indicator = 'Whiff'

        return indicator

    #Checks if entity is still alive
    def checkHealth(self):
        if self.health < 0:
            if abs(self.health) < self.baseHealth:
                self.alive = False
            else:
                self.unconscious = True
            self.health = 0
            
    #Heals the entity
    def heal(self, damage):
        (number,dice,bonus) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1,dice)
        appliedHealing = base + bonus
        self.health += appliedHealing
            
    #Resets the stats to the base stats
    def resetStats(self):
        self.stat = {}
        for stat in self.baseStat:
            self.stat[stat] = self.baseStat[stat]
        
    def resetMovement(self):
        self.movement = self.maxMovement
        
    #Recalculates the entity modifiers after a change of stats
    def refreshModifierStat(self):
        self.mod = {}
        for stat in self.stat:
            self.mod[stat] = int((self.stat[stat]-self.stat[stat]%2)/2)-5

    #Recalculates the entity AC
    def refreshArmourStat(self):
        if self.armour.type == 'Heavy':
            self.armourClass = self.armour.armourValue
        elif self.armour.type == 'Medium':
            self.armourClass = self.armour.armourValue + min(self.mod['DEX'],2)
        elif self.armour.type == 'Light':
            self.armourClass = self.armour.armourValue + self.mod['DEX']
        elif self.armour == None:
            self.armourClass = self.mod['DEX']
        
    #Recalculates the entity damage and reach
    def refreshWeaponStat(self):
        self.reach = self.primaryWeapon.reach
        if self.primaryWeapon.finesse:
            self.atkMod = max(self.mod['STR'],self.mod['DEX'])
        else:
            self.atkMod = self.mod['STR']
        self.damage = (self.primaryWeapon.damage[0], self.primaryWeapon.damage[1], self.atkMod)
        
    #Makes a saving throw
    def makeSavingThrow(self):
        throw = rd.randint(1,20)
        saved = False
        dies = False
        
        if throw == 1:
            self.savingThrows = (self.savingThrows[0],self.savingThrows[1]+2)
            output = 'Critical Fail'
        elif throw < 10:
            self.savingThrows = (self.savingThrows[0],self.savingThrows[1]+1)
            output = 'Fail'
        elif throw == 20:
            saved = True
            output = 'Critical Success!'
        else:
            self.savingThrows = (self.savingThrows[0]+1,self.savingThrows[1])
            output = 'Success!'
            
        if self.savingThrows[0] >= 3:
            saved = True
        elif self.savingThrow[1] >= 3:
            dies = True
            
        if saved:
            self.health = 1
            self.stable = True
            output = 'Saved'
        if dies:
            self.dead = True
            output = 'Died'
            
        return output
    
    #Collects entity end stats
    def overrideStats(self): # temporary measure to work with just these stats
        self.baseSize = 
        self.health = 
        self.armourClass = 
        self.primaryWeapon = 
        self.atkMod = 
        self.profBonus = 
        self.maxMovement = 
        
    #Collects entity base stats
    def getStats(self): # yet to get from jamie
        super().getStats(self)
        self.lvl
        self.maxMovement
        self.type
        
        self.armour
        self.primaryWeapon
        
#A playable character        
class Player(AnimateEntity):
    def __init__(self, playerName, entityID, playerLevel = 1, playerClass = None):
        super().__init__(self, playerName, entityID)
        self.lvl = playerLevel
        self.type = playerClass

    #Recalculates the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.profBonus = int(((self.lvl-1)-(self.lvl-1)%4)/4)+2
        self.calcHealth()

    #Calculates health based on level and con mod
    def calcHealth(self):
        self.baseHealth = self.con+self.hitDiceValue + (self.lvl-1)*(self.mod['CON']+0.5+self.hitDiceValue/2)

#A non-playable character        
class NPC(AnimateEntity):
    def __init__(self, npcName, entityID):
        super().__init__(self, npcName, entityID)
        self.target = None

#A hostile character        
class Monster(NPC):
    def __init__(self, monsterName, entityID):
        super().__init__(self, monsterName, entityID)
        
    #Checks if entity is still alive
    def checkHealth(self):
        if self.health < 0:
            self.alive = False
            self.health = 0