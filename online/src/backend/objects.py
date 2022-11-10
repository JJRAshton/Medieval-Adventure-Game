import random as rd

class Entity:
    def __init__(self, entityName):
        self.name = entityName
        self.id = 0

        self.baseSize = 5
        self.weight = 0
        self.weightTotal = 0
        
        self.baseHealth = 0
        self.health = 0

        self.armourClass = 0
        
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
        if self.health <= 0:
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
    def __init__(self, objectName):
        super().__init__(self, objectName)

    def getStats(self):
        super().getStats(self)
        self.armourClass

class Item(Entity):
    def __init__(self, itemName):
        super().__init__(self, itemName)
        self.is_carried = True
        
class Weapon(Item):
    def __init__(self, weaponName):
        super().__init__(self, weaponName)
        self.damage = (0,0)
        self.reach = 5
        
        self.is_ranged = False
        
        self.is_loading = False
        self.is_arrows = False
        self.is_bolts = False
        self.is_light = False
        self.is_heavy = False
        self.is_versitile = False
        self.is_finesse = False
    
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
        
class Armour(Item):
    def __init__(self, armourName):
        super().__init__(self, armourName)
        self.type = ''
        self.armourValue = 0
    
    #Collects entity base stats
    def getStats(self): # yet to get from jamie
        super().getStats(self)
        self.type
        self.armourValue