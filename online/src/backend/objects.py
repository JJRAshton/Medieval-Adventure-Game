import random as rd
from backend.stat_collection import Stats


class Entity:
    entityStats = Stats()

    def __init__(self, entityName):
        self.name = entityName
        self.id = 0

        self.baseSize = 5
        self.size = 5

        self.baseHealth = 0
        self.health = 0

        self.armourClass = 0

        self.is_alive = True
        
        self.coords = (0, 0)
        
        self.resetSize()
    
    # Moves to new coords
    def move(self, vector):
        self.coords = (self.coords[0]+vector[0], self.coords[1]+vector[1])
            
    def resetHealth(self):
        self.health = self.baseHealth
    
    def resetSize(self):
        self.size = self.baseSize
    
    # Checks if entity is still alive
    def checkHealth(self):
        if self.health <= 0:
            self.is_alive = False
            self.health = 0
            
    # Damages the entity
    def takeDamage(self, damage):
        (number, dice, bonus) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1, dice)
        appliedDamage = base + bonus
        self.health -= appliedDamage
        
        self.checkHealth()
        
        return appliedDamage


class Object(Entity):
    def __init__(self, objectName):
        super().__init__(objectName)

        self.getStats()

    def getStats(self):
        Entity.entityStats.getObjectStats(self)


class Item(Entity):
    def __init__(self, itemName):
        super().__init__(itemName)
        self.is_carried = True


class Weapon(Item):
    def __init__(self, weaponName):
        super().__init__(weaponName)
        self.damage = (0, 0)
        self.reach = 5
        
        self.is_ranged = False
        
        self.is_loading = False
        self.is_arrows = False
        self.is_bolts = False
        self.is_light = False
        self.is_heavy = False
        self.is_versatile = False
        self.is_finesse = False
        
        self.getStats()
    
    # Collects entity base stats
    def getStats(self):  # yet to get from jamie
        Entity.entityStats.getWeaponStats(self)


class Armour(Item):
    def __init__(self, armourName):
        super().__init__(armourName)
        self.type = ''
        self.armourValue = 0
        
        self.getStats()
    
    # Collects entity base stats
    def getStats(self):  # yet to get from jamie
        Entity.entityStats.getArmourStats(self)
