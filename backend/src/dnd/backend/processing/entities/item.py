from .entity import Entity


class Item(Entity):

    def __init__(self, itemName: str, id: str):
        super().__init__(itemName, id, size=5)
        self.is_carried = True
        self.type = ''


class Weapon(Item):

    ''' Don't construct directly, use WeaponFactory instead '''
    def __init__(self, weaponName: str, id: str, damage_dice, attack_range, attacks, protection, defense_type, traits):
        super().__init__(weaponName, id)
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

    def __init__(self, armourName: str, id: str, armour_type, value, flex, weight, material, coverage, bulk):
        super().__init__(armourName, id)
        self.type = armour_type
        self.value = value
        self.flex: float = flex
        self.weight = weight
        self.material = material
        self.coverage = coverage
        self.bulk = bulk
