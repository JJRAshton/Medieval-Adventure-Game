import random as rd

from .character import Character
from .classes.player_class import PlayerClass


# A playable character
class Player(Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']

    def __init__(self, player_class: PlayerClass, weapon_factory, player_name: str, base_attacks, base_stats, equipped_weapons):
        super().__init__(
            player_name,
            weapon_factory=weapon_factory,
            base_attacks=base_attacks,
            base_stats=base_stats,
            equipped_weapons=equipped_weapons
        )
        self.p_class = player_class
        self.equipped_armour = self.p_class.startingArmour
        self.base_movement = self.p_class.base_movement
        self.skill = self.p_class.skill
        if self.has_Trait('Slow'):
            self.actions_total = 1

    def resetStats(self):
        super().resetStats()
        if self.has_Trait('Strong'):
            self.stat['STR'] = int(1.2 * self.stat['STR'])

    # Unequips a weapon if one present in given location
    def unequipWeapon(self, location):
        weapon = self.equipped_weapons[location]
        if weapon is not None:
            self.equipped_weapons[location] = None
            self.inventory.append(weapon)

    # Equips a weapon
    def equipWeapon(self, invIndex, location):
        weapon = self.inventory[invIndex]

        if not weapon.is_Weapon():
            return

        if weapon.has_trait('Two-handed'):
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
    def unequip_armour(self, armour_type):
        armour = self.equipped_armour[armour_type]
        if armour is not None:
            self.equipped_armour[armour_type] = None
            self.inventory.append(armour)

    # Equip a set of armour
    def equipArmour(self, inv_index):
        armour = self.inventory[inv_index]

        if not armour.is_Armour:
            return

        self.unequip_armour(armour.p_class)

        self.equipped_armour[armour.p_class] = armour

        self.inventory.pop(inv_index)

    # Resets evasion accounting for bonus melee evasion of some classes
    def resetEvasion(self):
        base_evasion = self.base_evasion

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

    # Calculates health based on CON and class
    def calcHealth(self):
        self.baseHealth = round(self.stat['CON'] * self.p_class.health_modifier)

    # Calculates evasion based on DEX class
    def calcEvasion(self):
        self.base_evasion = int(self.stat['DEX'] * self.p_class.evasion_modifier)

    # Checks if the player is proficient with the weapon
    def is_Proficient(self, weapon):
        return weapon.type in self.p_class.weapons
