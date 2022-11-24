import random as rd

from .stats import EntityStats
from . import attack as at


class Entity:
    entityStats = EntityStats()

    def __init__(self, entityName):
        self.name = entityName
        self.id = 0

        self.baseSize = 5
        self.size = 0
        
        self.coords = (0, 0)
    
    # Moves to new coords
    def move(self, vector):
        self.coords = (self.coords[0]+vector[0], self.coords[1]+vector[1])
    
    def resetSize(self):
        self.size = self.baseSize


class HealthEntity(Entity):
    def __init__(self, entityName):
        super().__init__(entityName)

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

    # Checks if entity is still alive
    def checkAlive(self):
        if self.health <= 0:
            self.is_alive = False
            self.health = 0

    # Resets health to base health
    def resetHealth(self):
        self.health = self.baseHealth

    # Damages the entity
    def takeDamage(self, damage, dmg_type, is_AP=False, critical=False):
        appliedDamage = damage

        armour = 0
        if not critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
            if is_AP:
                armour *= 0.75

        armour = int(armour)
        appliedDamage -= armour

        if dmg_type in self.vulnerabilities:
            appliedDamage *= 2
        elif dmg_type in self.resistances:
            appliedDamage *= 0.5

        if appliedDamage > 0:
            self.health -= int(appliedDamage)
            self.checkAlive()
        else:
            appliedDamage = 0

        return appliedDamage


class Object(HealthEntity):
    def __init__(self, objectName):
        super().__init__(objectName)

        self.getStats()
        self.resetHealth()
        self.resetSize()

    def getStats(self):
        Entity.entityStats.getObjectStats(self)
