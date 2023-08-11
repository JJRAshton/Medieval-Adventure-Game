from typing import List
from .character import Character

# A non-playable character
class NPC(Character):
    def __init__(self, npcName: str, base_attacks, base_stats, equipped_weapons,
                 equipped_armour, vulnerabilities, resistances, base_movement):
        self.target = None
        self.behaviour_type = 2
        self.team = 1
        self.max_bulk = 20

        # Only weapon proficiencies for now
        self.item_proficiencies = [weapon.name for weapon in equipped_weapons.values() if weapon]
        self.vulnerabilities: List[str] = vulnerabilities
        self.resistances: List[str] = resistances

        super().__init__(
            npcName,
            base_attacks=base_attacks,
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
            equipped_armour=equipped_armour,
            vulnerabilities=vulnerabilities,
            resistances=resistances,
            base_movement=base_movement
        )

    def setup(self):
        self.reset_health()
        self.refreshStatAfterEquipment()
        self.calcInitiative()

    # Checks if the character is proficient with the weapon
    def is_Proficient(self, weapon):
        return weapon.name in self.item_proficiencies

    # Sees if the npc max bulk has been exceeded
    def is_exceededBulk(self):
        return self.bulk > self.max_bulk


# A hostile character
class Monster(NPC):
    def __init__(self, monsterName: str, base_attacks, base_stats, equipped_weapons,
                 equipped_armour, vulnerabilities, resistances, base_movement):
        super().__init__(
            monsterName,
            base_attacks=base_attacks,
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
            equipped_armour=equipped_armour,
            vulnerabilities=vulnerabilities,
            resistances=resistances,
            base_movement=base_movement
        )
        self.team = 2

    # Checks if entity is still alive
    def check_alive(self):
        if self.health < 0:
            self.is_alive = False
            self.health = 0
