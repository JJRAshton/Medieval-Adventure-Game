import random as rd

from . import character as ch
from . import classes as cl


# A playable character
class Player(ch.Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']

    p_classes = {
        'Raider': cl.Raider,
        'Gladiator': cl.Gladiator,
        'Guardian': cl.Guardian,
        'Knight': cl.Knight,
        'Samurai': cl.Samurai,
        'Hunter': cl.Hunter,
        'Professor': cl.Professor,
        'Ninja': cl.Ninja
        }

    def __init__(self, player_class, player_name):
        super().__init__(player_name)
        self.p_class = player_class

    def resetStats(self):
        super().resetStats()
        if self.has_Trait('Strong'):
            self.stat['STR'] = int(1.2 * self.stat['STR'])

    # Gets the player class associated stats
    def getClass(self):
        self.equippedArmour = self.p_class.startingArmour
        self.baseMovement = self.p_class.baseMovement
        self.skill = self.p_class.skill
        if self.has_Trait('Slow'):
            self.actionsTotal = 1

    # Unequips a weapon if one present in given location
    def unequipWeapon(self, location):
        weapon = self.equipped_weapons[location]
        if weapon is not None:
            self.equipped_weapons[location] = None
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
    def equipSingleWeapon(self, inv_index, location):
        weapon = self.inventory[inv_index]

        self.unequipWeapon('Both')
        self.unequipWeapon(location)

        self.equipped_weapons[location] = weapon

        self.inventory.pop(inv_index)

    # Equips a two-handed weapon
    def equipDoubleWeapon(self, invIndex):
        weapon = self.inventory[invIndex]

        for location in self.equipped_weapons:
            self.unequipWeapon(location)

        self.equipped_weapons['Both'] = weapon

        self.inventory.pop(invIndex)

    # Unequip a set of armour
    def unequipArmour(self, armour_type):
        armour = self.equippedArmour[armour_type]
        if armour is not None:
            self.equippedArmour[armour_type] = None
            self.inventory.append(armour)

    # Equip a set of armour
    def equipArmour(self, inv_index):
        armour = self.inventory[inv_index]

        if not armour.is_Armour:
            return

        self.unequipArmour(armour.p_class)

        self.equippedArmour[armour.p_class] = armour

        self.inventory.pop(inv_index)

    # Resets evasion accounting for bonus melee evasion of some classes
    def resetEvasion(self):
        base_evasion = self.baseEvasion

        if self.has_Trait('Melee_evader'):
            self.evasion['Melee'] = int(base_evasion * (1 + self.stat['WIT'] / 100))
        else:
            self.evasion['Melee'] = int(base_evasion)

        if self.has_Trait('Ranged_evader'):
            self.evasion['Ranged'] = int(base_evasion * (1 + self.stat['WIT'] / 100))
        else:
            self.evasion['Ranged'] = int(base_evasion)

    # Allows for finding the class traits of a player
    def has_Trait(self, trait_str):
        return trait_str in self.p_class.traits

    # Returns if the max bulk has been exceeded
    def is_exceededBulk(self):
        return self.bulk > self.p_class.max_bulk

    # Calculates the entity proficiency bonus
    def calcProfB(self):
        self.hitProf = 10

    # Calculates health based on CON and class
    def calcHealth(self):
        self.baseHealth = round(self.stat['CON'] * self.p_class.health_modifier)

    # Calculates evasion based on DEX class
    def calcEvasion(self):
        self.baseEvasion = int(self.stat['DEX'] * self.p_class.evasion_modifier)

    # Checks if the player is proficient with the weapon
    def is_Proficient(self, weapon):
        return weapon.type in self.p_class.weapons
