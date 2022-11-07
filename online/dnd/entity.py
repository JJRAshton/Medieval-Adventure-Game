import random as rd

class Entity:
    def __init__(self):
        self.baseSize = 5
        self.weight = 0
        self.weightTotal = 0
        
        self.baseHealth = 0
        self.health = 0
        
        self.alive = True
        
        self.texture = None
        
        self.coords = (0,0)
    
    #Moves to new coords           
    def move(self, vector):
        self.coords = (self.coords[0]+vector[0],self.coords[1]+vector[1])
            
    def resetHealth(self):
        self.health = self.baseHealth
    
    def resetSize(self):
        self.size = self.baseSize
    
    #Checks if entity is still alive
    def checkHealth(self):
        if self.health < 0:
            self.alive = False
            self.health = 0
            
    #Damages the entity
    def takeDamage(self, damage):
        (number,dice,bonus) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1,dice)
        appliedDamage = base + bonus
        self.health -= appliedDamage
        
        self.checkHealth()
        
    #Collects entity base stats
    def getStats(self):
        print('hello world!')
        
    #Collects entity end stats
    def overrideStats(self):
        print('ahh')
        
class MovingEntity(Entity):
    def __init__(self):
        super().__init__(self)
        self.lvl = 0
        self.maxMovement = 0
        self.type = None
        
        self.baseStrStat = 0
        self.baseDexStat = 0
        self.baseConStat = 0
        self.baseIntStat = 0
        self.baseWisStat = 0
        self.baseCharStat = 0
        
        self.hitDiceValue = 0
        self.hitDiceNumber = 0
        
        self.primaryWeapon = None
        self.armour = None
        
        self.movement = 0
        
        self.unconscious = False
        self.savingThrows = (0,0)
        
        self.inventory = []
        
        self.levelUp()
        self.refreshModifierStat()
        self.refreshArmourStat()
        self.refreshWeaponStat()
    
    #Moves entity by given vector and decreases movement
    def move(self, vector):
        super().move(vector)
        count = abs(vector[0])+abs(vector[1])
        self.movement -= 5*count
        
    #Checks if player is still alive
    def checkHealth(self):
        if self.health < 0:
            if abs(self.health) < self.baseHealth:
                self.alive = False
            else:
                self.unconscious = True
            self.health = 0
        
    #Resets the stats to the base stats
    def resetStats(self):
        self.strStat = self.baseStrStat
        self.dexStat = self.baseDexStat
        self.conStat = self.baseConStat
        self.intStat = self.baseIntStat
        self.wisStat = self.baseWiseStat
        self.charStat = self.baseCharStat
        
    def resetMovement(self):
        self.movement = self.maxMovement
        
    #Recalculates the entity stats after a change of stats
    def refreshModifierStat(self):
        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.char = 0
    
    #Recalculats the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.baseHealth = self.con+self.hitDiceValue + (self.lvl-1)*(self.con+0.5+self.hitDiceValue/2)
    
    #Recalculates the entity stats after change of armour
    def refreshArmourStat(self):
        if self.armour.type == 'Heavy':
            self.AC = self.armour.armourValue
        elif self.armour.type == 'Medium':
            self.AC = self.armour.armourValue + min(self.dex,2)
        elif self.armour.type == 'Light':
            self.AC = self.armour.armourValue + self.dex
        elif self.armour == None:
            self.AC = self.dex
        
    #Recalculates the creature stats after change of weapon
    def refreshWeaponStat(self):
        self.damage = self.primaryWeapon.damage + self.str
        self.reach = self.primaryWeapon.reach
        
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
        
        
class Object(Entity):
    def __init__(self):
        super().__init__(self)
        self.weight = 0
        
class Weapon(Object):
    def __init__(self):
        super().__init__(self)
        self.damage = 0
        self.reach = 5
        
        self.loading = False
        self.ammunition = False
        self.light = False
        self.heavy = False
        
class Armour(Object):
    def __init__(self):
        super().__init__(self)
        self.type = ''
        self.armourValue = 0

#A playable character        
class Player(MovingEntity):
    def __init__(self):
        super().__init__(self)

#A non-playable character        
class Creature(MovingEntity):
    def __init__(self):
        super().__init__(self)

#A hostile character        
class Monster(Creature):
    def __init__(self):
        super().__init__(self)
        
    #Checks if entity is still alive
    def checkHealth(self):
        if self.health < 0:
            self.alive = False
            self.health = 0