from typing import List
from .character import Character

# A non-playable character
class NPC(Character):
    def __init__(self, npcName: str, base_attacks, base_stats, equipped_weapons, equipped_armour, vulnerabilities, resistances):
        self.target = None
        self.behaviour_type = 2
        self.team = 1
        self.max_bulk = 20

        self.item_profficiencies = [] # List of names of things this Character is profficient with

        self.vulnerabilities: List[str] = vulnerabilities
        self.resistances: List[str] = resistances

        super().__init__(
            npcName,
            base_attacks=base_attacks,
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
            equipped_armour=equipped_armour
        )

    # Checks if the character is proficient with the weapon
    def is_Proficient(self, weapon):
        return weapon.name in self.item_profficiencies

    # Sees if the npc max bulk has been exceeded
    def is_exceededBulk(self):
        return self.bulk > self.max_bulk


# A hostile character
class Monster(NPC):
    def __init__(self, monsterName: str, base_attacks, base_stats, equipped_weapons, equipped_armour, vulnerabilities, resistances):
        super().__init__(
            monsterName,
            base_attacks=base_attacks,
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
            equipped_armour=equipped_armour,
            vulnerabilities=vulnerabilities,
            resistances=resistances
        )
        self.team = 2

    # Checks if entity is still alive
    def check_alive(self):
        if self.health < 0:
            self.is_alive = False
            self.health = 0
