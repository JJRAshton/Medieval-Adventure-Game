from .stats import assign_attack as st


class Attack:
    stats = st.AttackStats()

    def __init__(self, atk_name):
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
