import pandas as pd
import os


inputs_dir = os.path.dirname(__file__) + '/../../../../../resources/inputs'


class Class:

    def __init__(self):
        self.name = ''
        self.stat_order = []
        self.weapons = []
        self.traits = []

        self.max_bulk = 0
        self.health_modifier = 0
        self.evasion_modifier = 0
        self.skill = 0

        self.baseMovement = 0
        self.startingArmour = {
            'Under': None,
            'Over': None
        }

    # Gets the associated stats of the class
    def getStats(self):
        class_table = pd.read_csv(f'{inputs_dir}/classes.csv', keep_default_na=False, index_col='Name')
        class_dict = class_table.loc[self.name].to_dict()

        self.health_modifier = float(class_dict['Health Mod'])
        self.evasion_modifier = float(class_dict['Evasion Mod'])
        self.max_bulk = int(class_dict['Max Bulk'])
        self.skill = int(class_dict['Skill'])

        self.baseMovement = int(class_dict['Base Movement'])

        if class_dict['Armour']:
            if ', ' in class_dict['Armour']:
                under, over = class_dict['Armour'].split(', ')
                self.startingArmour['Under'] = under
                self.startingArmour['Over'] = over
            else:
                self.startingArmour['Under'] = class_dict['Armour']
