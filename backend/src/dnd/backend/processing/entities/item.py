from .entity import Entity


class Item(Entity):

    def __init__(self, itemName):
        super().__init__(itemName)
        self.is_carried = True
        self.type = ''


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

    def __init__(self, armourName, armour_type, value, flex, weight, material, coverage, bulk):
        super().__init__(armourName)
        self.type = armour_type
        self.value = value
        self.flex: float = flex
        self.weight = weight
        self.material = material
        self.coverage = coverage
        self.bulk = bulk
