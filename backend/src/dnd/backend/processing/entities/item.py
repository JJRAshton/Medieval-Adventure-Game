from .entity import Entity
from .stats.make_dataframes import weapon_types


class Item(Entity):

    def __init__(self, itemName):
        super().__init__(itemName)
        self.is_carried = True
        self.type = ''

    # Checks if the item is a weapon
    def is_Weapon(self):
        return self.type in weapon_types

    # Checks if the item is armour
    def is_Armour(self):
        return self.type in ['Under', 'Over']


class Weapon(Item):

    ''' Don't construct directly, use WeaponFactory instead '''
    def __init__(self, weaponName: str, damage_dice, attack_range, attacks, protection, defense_type, traits):
        super().__init__(weaponName)
        self.damage_dice = damage_dice
        self.range = attack_range

        self.attacks = attacks

        self.protection = protection
        self.defense_type = defense_type

        self.traits = traits

    def has_trait(self, trait: str):
        return trait in self.traits


''' Don't create directly, use EntityFactory. '''
class Armour(Item):

    def __init__(self, armourName):
        super().__init__(armourName)
        self.type = ''
        self.value = 0
        self.flex: float = 0
        self.weight = 0
        self.material = ''
        self.coverage = 0
        self.bulk = 0
