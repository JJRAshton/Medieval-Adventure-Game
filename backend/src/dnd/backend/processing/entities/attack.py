from ...utils import dice_utils

class AttackType:
    
    def __init__(self, type_name: str):
        self.__type_name = type_name

    def get_name(self) -> str:
        return self.__type_name


class AttackTypes:
    RAW = AttackType('raw')
    WEAPON = AttackType('weapon')

class Attack:

    ''' An attack, don't construct this directly, use AttackFactory instead '''
    def __init__(self, atk_name: str, attack_type, damage, damage_types, damage_maintype):
        self.name = atk_name
        self.type = attack_type  # Raw or Weapon attack

        self.damage = damage
        self.damage_types = damage_types  # Contains the types of damage with their percentages
        self.damage_maintype = damage_maintype  # The main type of damage for hit contests
        self.avdmg = self.damage[0] * (self.damage[1] + 1) / 2

        self.id = 0
        self.from_weapon = None

    def updateDamage(self):
        if self.type == 'weapon' and self.from_weapon is not None:
            self.damage = (self.damage[0], self.from_weapon.damage_dice)

        self.avdmg = self.damage[0] * (self.damage[1] + 1) / 2
        self.damage_maintype = max(self.damage_types, key=self.damage_types.get)

    def setWeapon(self, weapon):
        self.from_weapon = weapon

    # Rolls for the damage to an entity
    def rollDamage(self, dmg_stat, dmg_mult=1):
        number, dice = self.damage

        # Increases it according to the damage stat
        totalDamage = dmg_mult * dice_utils.roll_dice(number, dice) * (1 + (dmg_stat - 25) / 100)

        # self.damage_types scaled by the rolled damage
        return {damage_type: totalDamage * self.damage_types[damage_type] for damage_type in self.damage_types}
