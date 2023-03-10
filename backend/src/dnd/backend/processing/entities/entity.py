from typing import Tuple
from .stats import EntityStats


class Entity:
    entityStats = EntityStats()

    def __init__(self, entityName: str):
        self.name = entityName
        self.id = 0

        self.baseSize = 5
        self.size = 0
        
        self.coords = (0, 0)

    def __eq__(self, other: object):
        return self.id == other
    
    # Moves to new coords
    def move(self, vector: Tuple[int, int]):
        self.coords = (self.coords[0]+vector[0], self.coords[1]+vector[1])
    
    def resetSize(self):
        self.size = self.baseSize


class HealthEntity(Entity):
    def __init__(self, entityName: str):
        super().__init__(entityName)

        self.baseHealth = 0
        self.maxHealth = 0
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
        self.maxHealth = self.baseHealth
        self.health = self.maxHealth

    # Damages the entity
    def takeDamage(self, damage, dmg_type, is_AP=False, is_critical=False, AA_stat=None):
        appliedDamage = damage

        armour = 0
        if not is_critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
            if is_AP:
                armour *= 0.8
            if AA_stat:
                armour *= 1 - AA_stat / 100

        armour = int(armour)
        appliedDamage -= armour

        if dmg_type in self.vulnerabilities:
            appliedDamage *= 2
        elif dmg_type in self.resistances:
            appliedDamage *= 0.5

        appliedDamage = round(appliedDamage)
        if appliedDamage > 0:
            self.health -= appliedDamage
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
