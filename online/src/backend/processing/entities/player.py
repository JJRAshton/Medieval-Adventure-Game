import random as rd

from . import character as ch
from . import entity as ent
from . import classes as cl


# A playable character
class Player(ch.Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']

    p_classes = {
        'Raider': cl.Raider,
        'Gladiator': cl.Gladiator,
        'Ranger': cl.Ranger,
        'Knight': cl.Knight,
        'Hunter': cl.Hunter,
        'Professor': cl.Professor,
        'Ninja': cl.Ninja
        }

    def __init__(self, playerClass=None, playerName=None):
        if playerName is None:
            playerName = rd.choice(Player.names)
        self.p_class = Player.p_classes[playerClass]()

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

        self.unequipArmour(armour.p_class)

        self.equippedArmour[armour.p_class] = armour

        self.inventory.pop(invIndex)

    # Calculates the entity proficiency bonus
    def calcProfB(self):
        self.hitProf = 10

    # Calculates health based on level and con mod
    def calcHealth(self):
        self.baseHealth = 2 * self.stat['CON']
        self.maxHealth = self.baseHealth

    # Checks if the player is proficient with the weapon
    def is_Proficient(self, weapon):
        if weapon.type in self.p_class.weapons:
            return True
        else:
            return False