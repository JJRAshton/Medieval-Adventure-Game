import random as rd

from .stats import assign_attack as st


class Attack:
    stats = st.AttackStats()

    def __init__(self, atk_name: str):
        self.name = atk_name
        self.type = ''  # Raw or Weapon attack

        self.damage = (0, 0)
        self.damage_types = {}  # Contains the types of damage with their percentages
        self.damage_maintype = ''  # The main type of damage for hit contests
        self.avdmg = 0

        self.id = 0
        self.from_weapon = None

        self.getStats()

    def getStats(self):
        Attack.stats.getAttackStats(self)

    def updateDamage(self):

        if self.type == 'weapon' and self.from_weapon is not None:
            dice_no = self.damage[0]
            self.damage = (dice_no, self.from_weapon.damage_dice)

        self.avdmg = self.damage[0] * (self.damage[1] + 1) / 2

        current_percent = 0
        for dmg_type in self.damage_types:
            if self.damage_types[dmg_type] > current_percent:
                self.damage_maintype = dmg_type

    def setWeapon(self, weapon):
        self.from_weapon = weapon

    # Rolls for the damage to an entity
    def rollDamage(self, dmg_stat, dmg_mult=1):
        number, dice = self.damage

        # Roll for base damage
        base = 0
        for _ in range(number):
            base += rd.randint(1, dice)

        # Increases it according to the damage stat
        totalDamage = dmg_mult * base * (1 + (dmg_stat - 25) / 100)

        damage = {}
        for damage_type in self.damage_types:
            damage[damage_type] = totalDamage * self.damage_types[damage_type]

        return damage
