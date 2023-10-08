from typing import List
import pandas as pd
import os


inputs_dir = os.path.dirname(__file__) + '/../../../../../../resources/inputs'


class PlayerClass:

    def __init__(self, name: str, stat_order: List[str], weapons: List[str], traits: List[str]):
        self.name = name
        self.stat_order = stat_order
        self.weapons = weapons
        self.traits = traits

        self.max_bulk = 0
        self.health_modifier = 0
        self.evasion_modifier = 0
        self.skill = 0

        self.baseMovement = 0
        self.startingArmour = {
            'Under': None,
            'Over': None
        }
        self.getStats() # This is probably not the best pattern

    # Gets the associated stats of the class
    def getStats(self):
        class_table = pd.read_csv(f'{inputs_dir}/classes.csv', keep_default_na=False, index_col='Name')
        class_dict = class_table.loc[self.name].to_dict()

        self.health_modifier = float(class_dict['Health Mod'])
        self.evasion_modifier = float(class_dict['Evasion Mod'])
        self.max_bulk = int(class_dict['Max Bulk'])
        self.skill = int(class_dict['Skill'])

        self.base_movement = int(class_dict['Base Movement'])

        if class_dict['Armour']:
            if ', ' in class_dict['Armour']:
                under, over = class_dict['Armour'].split(', ')
                self.startingArmour['Under'] = under
                self.startingArmour['Over'] = over
            else:
                self.startingArmour['Under'] = class_dict['Armour']

GLADIATOR = PlayerClass(
    'Gladiator', ['STR', 'DEX', 'CON', 'WIT'],
    ['arena_weapons', 'heavy_throwables'], ['Keen_eye', 'Savage_critical'])
GUARDIAN = PlayerClass( # shields
    'Guardian', ['CON', 'WIT', 'STR', 'DEX'],
    ['books', 'hammers'], ['Tank', 'Slow'])
HUNTER = PlayerClass( # bows
    'Hunter', ['WIT', 'DEX', 'STR', 'CON'],
    ['special', 'axes'], ['Ranged_evader', 'Melee_evader'])
KNIGHT = PlayerClass( # polearms, double_edged_swords
    'Knight', ['STR', 'CON', 'WIT', 'DEX'],
    ['polearms', 'double_edged_swords', 'spears'],['Armour_experience', 'Anti-armour_expert'])
NINJA = PlayerClass(
    'Ninja', ['DEX', 'WIT', 'STR', 'CON'],
    ['single_edged_swords', 'light_throwables', 'mythical'], ['Melee_evader'])
PROFESSOR = PlayerClass(
    'Professor', ['WIT', 'DEX', 'CON', 'STR'],
    ['staves', 'books', 'mythical'], [])
RAIDER = PlayerClass(
    'Raider', ['STR', 'CON', 'DEX', 'WIT'],
    ['glaives', 'axes', 'heavy_throwables'], ['Charged_hits', 'Strong'])
SAMURAI = PlayerClass(   # bows
    'Samurai', ['STR', 'DEX', 'WIT', 'CON'],
    ['single_edged_swords'], ['Melee_evader', 'Keen_eye']
) 

# Some of these may cause problems? I'm not sure. I should write a test...
ALL = [GLADIATOR, GUARDIAN, HUNTER, KNIGHT, NINJA, PROFESSOR, RAIDER, SAMURAI]