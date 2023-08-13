from typing import List, Optional

from .entity import Entity


class HealthEntity(Entity):
    def __init__(self, entity_name: str, id: str, max_health, vulnerabilities=[], resistances=[], size=5):
        super().__init__(entity_name, id, size)

        self.max_health = max_health
        self.health = 0

        self.vulnerabilities: List[str] = []
        self.resistances: List[str] = []

        self.armour = {
            'piercing': 0,
            'slashing': 0,
            'bludgeoning': 0
        }
        self.evasion = 0

        self.is_alive = True

    # Checks if entity is still alive
    def check_alive(self):
        if self.health <= 0:
            self.is_alive = False
            self.health = 0

    # Resets health to base health
    def reset_health(self):
        self.health = self.max_health

    # Damages the entity
    def take_damage(self, damage: float, dmg_type: str, is_AP: bool=False, is_critical: bool=False, AA_stat: Optional[float]=None):
        appliedDamage = damage

        armour: float = 0
        if not is_critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
            if is_AP:
                armour *= 0.8
            if AA_stat:
                armour *= 1 - AA_stat / 100

        armour = int(armour)
        appliedDamage -= armour

        if dmg_type in self.vulnerabilities:
            appliedDamage *= 2
        elif dmg_type in self.resistances:
            appliedDamage *= 0.5

        appliedDamage = round(appliedDamage)
        if appliedDamage > 0:
            self.health -= appliedDamage
            self.check_alive()
        else:
            appliedDamage = 0

        return appliedDamage