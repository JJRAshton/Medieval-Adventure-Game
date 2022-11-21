import random as rd

from .stats import EntityStats
from .session_functions import rollDamage
from . import attacks as at


class Entity:
    entityStats = EntityStats()

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
            'piercing': 0,
            'slashing': 0,
            'bludgeoning': 0
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
    def takeDamage(self, damage, dmg_type, heavy_hit=False, critical=False):
        appliedDamage = damage

        armour = 0
        if not critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
        if heavy_hit:
            if dmg_type == 'pierce':
                armour *= 0.5
            elif dmg_type == 'slash':
                appliedDamage *= 1.2

        armour = int(armour)
        appliedDamage -= armour

        if dmg_type in self.vulnerabilities:
            appliedDamage *= 2
        elif dmg_type in self.resistances:
            appliedDamage *= 0.5

        if appliedDamage > 0:
            self.health -= appliedDamage
            self.checkAlive()
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
        self.type = ''
        self.damage_dice = 0
        self.range = 0

        self.attacks = {}

        self.protection = 0
        self.defense_type = ''

        self.is_brutal = False
        self.is_ranged = False
        self.is_loading = False
        self.is_twoHanded = False
        self.is_arrows = False
        self.is_bolts = False
        self.is_light = False
        self.is_heavy = False
        self.is_finesse = False
        
        self.getStats()
    
    # Collects entity base stats
    def getStats(self):
        Entity.entityStats.getWeaponStats(self)
        attacks_list = []
        for attack_str in self.attacks:
            attack = at.Attack(attack_str)
            attack.from_weapon = self
            attacks_list.append(attack)


class Armour(Item):
    def __init__(self, armourName):
        super().__init__(armourName)
        self.type = ''
        self.value = 0
        self.restriction = 0
        self.weight = 0
        
        self.getStats()
    
    # Collects entity base stats
    def getStats(self):
        Entity.entityStats.getArmourStats(self)
