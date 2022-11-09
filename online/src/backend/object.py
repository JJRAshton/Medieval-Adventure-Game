import random as rd

class Entity:
    def __init__(self, entityName, entityID):
        self.name = entityName
        self.id = entityID

        self.baseSize = 5
        self.weight = 0
        self.weightTotal = 0
        
        self.baseHealth = 0
        self.health = 0
        
        self.inventory = []
        self.alive = True
        
        self.coords = (0,0)
        
        #self.getStats()
        self.resetSize()
        self.calcWeight()
        self.overrideStats()
    
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
        
        return appliedDamage
        
    #Collects entity base stats
    def getStats(self): # yet to get from jamie
        self.baseSize
        self.weight
        self.baseHealth
    
    #Calculates the entity weight
    def calcWeight(self):
        self.weightTotal = self.weight
        for item in self.inventory:
            self.weightTotal += item.weightTotal
        
class Object(Entity):
    def __init__(self, objectName, entityID):
        super().__init__(self, objectName, entityID)
        
class Weapon(Object):
    def __init__(self, weaponName, entityID):
        super().__init__(self, weaponName, entityID)
        self.damage = (0,0)
        self.reach = 5
        
        self.ranged = False
        
        self.loading = False
        self.arrows = False
        self.bolts = False
        self.light = False
        self.heavy = False
        self.versitile = False
        self.finesse = False
    
    #Collects entity base stats
    def getStats(self): # yet to get from jamie
        super().getStats(self)
        self.damage
        self.reach
        
        self.ranged
        
        self.loading
        self.arrows
        self.bolts
        self.light
        self.heavy
        self.finesse
        
    #Collects entity end stats
    def overrideStats(self): # temporary measure to work with just these stats
        self.damage = 
        self.reach = 
        
class Armour(Object):
    def __init__(self, armourName, entityID):
        super().__init__(self, armourName, entityID)
        self.type = ''
        self.armourValue = 0
    
    #Collects entity base stats
    def getStats(self): # yet to get from jamie
        super().getStats(self)
        self.type
        self.armourValue