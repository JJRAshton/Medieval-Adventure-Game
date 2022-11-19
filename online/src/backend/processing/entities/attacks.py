from stats import assign_attack as st


class Attack:
    stats = st.AttackStats()

    def __init__(self, atk_name):
        self.name = atk_name
        self.damage = (0, 0)
        self.damage_types = {}  # Contains the types of damage with their percentages

        self.getStats()

        self.avdmg = self.damage[0] * (self.damage[1] + 1) / 2

    def getStats(self):
        pass


class WepAttack(Attack):
    stats = st.AttackStats()

    def __init__(self, atk_name):
        super().__init__(atk_name)

    def getStats(self):
        WepAttack.stats.getWeaponAttackStats(self)


class RawAttack(Attack):
    stats = st.AttackStats()

    def __init__(self, atk_name):
        super().__init__(atk_name)

    def getStats(self):
        WepAttack.stats.getRawAttackStats(self)