from . import entity as ent
from . import attack as at
from .stats.make_dataframes import weapon_types


class Item(ent.Entity):

    def __init__(self, itemName):
        super().__init__(itemName)
        self.is_carried = True
        self.type = ''

    # Checks if the item is a weapon
    def is_Weapon(self):
        if self.type in weapon_types:
            return True
        else:
            return False

    # Checks if the item is armour
    def is_Armour(self):
        if self.type in ['Under', 'Over']:
            return True
        else:
            return False


class Weapon(Item):
    def __init__(self, weaponName):
        super().__init__(weaponName)
        self.damage_dice = 0
        self.range = 0
        self.holder_size = 0

        self.attacks = {}

        self.protection = 0
        self.defense_type = ''

        self.is_AP = False
        self.is_ranged = False
        self.is_loading = False
        self.is_twoHanded = False
        self.is_arrows = False
        self.is_bolts = False
        self.is_light = False
        self.is_finesse = False
        self.is_fine = False
        self.is_magic = False

        self.is_melee = True

        self.getStats()

    # Collects entity base stats
    def getStats(self):
        ent.Entity.entityStats.getWeaponStats(self)
        attacks_list = []
        for attack_str in self.attacks:
            attack = at.Attack(attack_str)
            attack.setWeapon(self)
            attack.updateDamage()
            attacks_list.append(attack)
        self.attacks = attacks_list


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

        self.getStats()

    # Collects entity base stats
    def getStats(self):
        ent.Entity.entityStats.getArmourStats(self)
