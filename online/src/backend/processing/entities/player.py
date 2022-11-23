import random as rd

from . import character as ch
from . import entity as ent


# A playable character
class Player(ch.Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']

    class_weapons = {
        'Beserker': ['axes', 'bludgeons', 'glaives'],
        'Gladiator': ['spears', 'mythical', 'throwables'],
        'Ranger': ['bows', 'double_edged_swords', 'special'],
        'Knight': ['hybrids', 'double_edged_swords', 'shields'],
        'Archer': ['bows', 'crossbows', 'throwables'],
        'Professor': ['staves', 'wands', 'mythical'],
        'Samurai': ['single_edged_swords', 'throwables', 'bows']
    }

    def __init__(self, playerLevel=1, playerClass=None, playerName=None):
        if playerName is None:
            playerName = rd.choice(Player.names)
        self.lvl = playerLevel
        self.type = playerClass
        self.healthDice = 0

        self.chosen_weapons = []

        self.behaviour_type = 1
        self.team = 1

        self.base_attacks = ['hit']

        super().__init__(playerName)

        self.getStats()

        self.resetStats()
        self.resetHealth()

        self.refreshStatAfterWeapon()
        self.refreshStatAfterArmour()

        self.calcInitiative()

        self.calcProfB()
        self.calcHealth()
        self.resetHealth()

    # Gets the player stats
    def getStats(self):
        ent.Entity.entityStats.getPlayerStats(self)
        self.getEquipment()
        self.convAttacks()
        self.getClass()

    # Recalculates the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.calcProfB()
        self.calcHealth()

    # Unequips a weapon if one present in given location
    def unequipWeapon(self, location):
        weapon = self.equippedWeapons[location]
        if weapon is not None:
            self.equippedWeapons[location] = None
            self.inventory.append(weapon)

    # Equips a weapon
    def equipWeapon(self, invIndex, location):
        weapon = self.inventory[invIndex]

        if not weapon.is_Weapon:
            return

        if weapon.is_twoHanded:
            self.equipDoubleWeapon(invIndex)
        else:
            self.equipSingleWeapon(invIndex, location)

    # Equips a one-handed weapon
    def equipSingleWeapon(self, invIndex, location):
        weapon = self.inventory[invIndex]

        self.unequipWeapon('Both')
        self.unequipWeapon(location)

        self.equippedWeapons[location] = weapon

        self.inventory.pop(invIndex)

    # Equips a two-handed weapon
    def equipDoubleWeapon(self, invIndex):
        weapon = self.inventory[invIndex]

        for location in self.equippedWeapons:
            self.unequipWeapon(location)

        self.equippedWeapons['Both'] = weapon

        self.inventory.pop(invIndex)

    # Unequip a set of armour
    def unequipArmour(self, armour_type):
        armour = self.equippedArmour[armour_type]
        if armour is not None:
            self.equippedArmour[armour_type] = None
            self.inventory.append(armour)

    # Equip a set of armour
    def equipArmour(self, invIndex):
        armour = self.inventory[invIndex]

        if not armour.is_Armour:
            return

        self.unequipArmour(armour.type)

        self.equippedArmour[armour.type] = armour

        self.inventory.pop(invIndex)

    # Calculates the entity proficiency bonus
    def calcProfB(self):
        self.hitProf = self.lvl * 5 + 5

    # Calculates health based on level and con mod
    def calcHealth(self):
        self.baseHealth = self.lvl * self.healthDice + self.stat['CON']
        self.maxHealth = self.baseHealth

    # Checks if the player is proficient with the weapon
    def is_Proficient(self, weapon):
        if weapon.type in self.chosen_weapons:
            return True
        else:
            return False

    # Gets the trait associated with the player's class
    def getClass(self):
        self.chosen_weapons = Player.class_weapons[self.type]