import random as rd

from .stats import Stats


class Entity:
    entityStats = Stats()

    def __init__(self, entityName):
        self.name = entityName
        self.id = 0

        self.baseSize = 5
        self.size = 5

        self.baseHealth = 0
        self.health = 0

        self.vulnerabilities = []
        self.resistances = []

        self.armour = {
            'pierce': 0,
            'slash': 0,
            'bludgeon': 0
        }
        self.evasion = 0

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
    def checkAlive(self):
        if self.health <= 0:
            self.is_alive = False
            self.health = 0


class Object(Entity):
    def __init__(self, objectName):
        super().__init__(objectName)

        self.getStats()

    def getStats(self):
        Entity.entityStats.getObjectStats(self)

    # Damages the entity
    def takeDamage(self, damage, bonus, dmg_type, heavy_hit = False, critical=False):
        (number, dice) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1, dice)

        if dmg_type in self.vulnerabilities:
            appliedDamage = 2*(base + bonus)
        elif dmg_type in self.resistances:
            appliedDamage = int(0.5*(base + bonus))
        else:
            appliedDamage = base + bonus

        armour = 0
        if not critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
        if heavy_hit:
            if dmg_type == 'pierce':
                armour *= 0.5
            elif dmg_type == 'slash':
                appliedDamage *= 1.2

        appliedDamage -= armour

        if appliedDamage > 0:
            self.health -= appliedDamage
            self.checkHealth()
        else:
            appliedDamage = 0

        return appliedDamage


class Item(Entity):
    def __init__(self, itemName):
        super().__init__(itemName)
        self.is_carried = True


class Weapon(Item):
    def __init__(self, weaponName):
        super().__init__(weaponName)
        self.damage = (0, 0)
        self.reach = 5
        self.dmg_type = ''
        self.type = ''
        
        self.is_ranged = False
        
        self.is_loading = False
        self.is_twoHanded = False
        self.is_arrows = False
        self.is_bolts = False
        self.is_light = False
        self.is_heavy = False
        self.is_finesse = False
        
        self.getStats()
        self.avdmg = self.damage[0] * (self.damage[1] + 1) / 2
    
    # Collects entity base stats
    def getStats(self):  # yet to get from jamie
        Entity.entityStats.getWeaponStats(self)


class Armour(Item):
    def __init__(self, armourName):
        super().__init__(armourName)
        self.type = ''
        self.value = 0
        self.restriction = 0
        self.weight = 0
        
        self.getStats()
    
    # Collects entity base stats
    def getStats(self):  # yet to get from jamie
        Entity.entityStats.getArmourStats(self)
