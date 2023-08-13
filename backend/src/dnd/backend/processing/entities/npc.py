from typing import List
from .character import Character
from ...utils import dice_utils

# A non-playable character, can be friendly or not
class NPC(Character):
    def __init__(self, npcName: str, id: str, base_attacks, base_stats, equipped_weapons,
                 equipped_armour, vulnerabilities, resistances, base_movement,
                 team, size, drop_rate, actions_total, base_armour, inventory,
                 difficulty, skill):
        self.target = None
        self.max_bulk = 20

        # Only weapon proficiencies for now
        self.item_proficiencies = [weapon.name for weapon in equipped_weapons.values() if weapon]
        self.vulnerabilities: List[str] = vulnerabilities
        self.resistances: List[str] = resistances
        self.drop_rate = drop_rate
        self.difficulty = difficulty

        super().__init__(
            npcName,
            id=id,
            base_attacks=base_attacks,
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
            equipped_armour=equipped_armour,
            vulnerabilities=vulnerabilities,
            resistances=resistances,
            base_movement=base_movement,
            team=team,
            behaviour_type=2,
            size=size,
            actions_total=actions_total,
            base_armour=base_armour,
            inventory=inventory,
            max_health=dice_utils.roll_dice(difficulty, base_stats['CON'], base_stats['CON']),
            skill=skill
        )

        self.reset_health()
        self.refreshStatAfterEquipment()
        self.calcInitiative()

    # Checks if the character is proficient with the weapon
    def is_Proficient(self, weapon):
        return weapon.name in self.item_proficiencies

    # Sees if the npc max bulk has been exceeded
    def is_exceededBulk(self):
        return self.bulk > self.max_bulk
    
    def check_alive(self):
        if self.team == 1:
            super().check_alive()
        else:
            if self.health < 0:
                self.is_alive = False
                self.health = 0
