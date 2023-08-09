from . import entity as ent
from .character import Character

# A non-playable character
class NPC(Character):
    def __init__(self, npcName: str, base_attacks, base_stats):
        self.target = None
        self.behaviour_type = 2
        self.team = 1
        self.max_bulk = 20

        self.starting_items = []

        super().__init__(
            npcName,
            base_attacks=base_attacks,
            base_stats=base_stats
        )

    # Checks if the character is proficient with the weapon
    def is_Proficient(self, weapon):
        return weapon.name in self.starting_items

    # Sees if the npc max bulk has been exceeded
    def is_exceededBulk(self):
        return self.bulk > self.max_bulk


# A hostile character
class Monster(NPC):
    def __init__(self, monsterName: str, base_attacks, base_stats):
        super().__init__(
            monsterName,
            base_attacks=base_attacks,
            base_stats=base_stats
        )
        self.team = 2

    # Checks if entity is still alive
    def check_alive(self):
        if self.health < 0:
            self.is_alive = False
            self.health = 0
