from typing import Dict, List
import pandas as pd
import os

INPUTS_DIR = os.path.dirname(__file__) + '/../../../../../../resources/inputs'

weapon_types = ['arena_weapons',
                'axes', 'clubs', 'hammers',
                'bows', 'crossbows', 'light_throwables', 'heavy_throwables',
                'shields', 'single_edged_swords', 'double_edged_swords', 'edgeless_swords',
                'glaives', 'polearms', 'spears',
                'special',  'mythical',
                'staves', 'books']


class EntityCSVToDataFrameParser():

    def make_weapon_stat_table(self):
        weapon_table = pd.DataFrame()
        for weapon_type in weapon_types:
            weapon_type_table = pd.read_csv(f'{INPUTS_DIR}/weapons/{weapon_type}.csv', keep_default_na=False, index_col='Name')
            weapon_type_table['Type'] = weapon_type
            weapon_table = pd.concat([weapon_table, weapon_type_table])
        return weapon_table.fillna('')


    def make_armour_stat_table(self):
        # read combat setup
        return pd.read_csv(f'{INPUTS_DIR}/armour.csv', keep_default_na=False, index_col='Name') # type: ignore


    def make_object_stat_table(self): # Unused?
        # read combat setup
        return pd.read_csv(f'{INPUTS_DIR}/objects.csv', keep_default_na=False, index_col='Name') # type: ignore


class EntityStatDictionaryProvider:

    def __init__(self):
        ''' Provides dictionaries containing stats for "Entities" (everything
        except attacks and weapons?) '''
        data_frame_factory = EntityCSVToDataFrameParser()
        self.__armour = data_frame_factory.make_armour_stat_table()
        self.__objects = data_frame_factory.make_object_stat_table() # unused?
        self.weapons = data_frame_factory.make_weapon_stat_table()

    def get_weapon_stats_dict(self, weapon_name: str) -> Dict[str, str]:
        # Make a dictionary of the stats for the entity
        return self.weapons.loc[weapon_name].to_dict() # type: ignore

    def get_armour_stats_dict(self, armour_name: str) -> Dict[str, str]:
        # Make a dictionary of the stats for the entity
        return self.__armour.loc[armour_name].to_dict() # type: ignore


class AttackCSVToDataFrameParser:

    def make_raw_attack_stat_table(self) -> pd.DataFrame:

        attack_table = pd.read_csv(f'{INPUTS_DIR}/raw_attacks.csv', keep_default_na=False, index_col='Name') # type: ignore

        attack_table.dropna(how='all', inplace=True) # type: ignore
        attack_table = attack_table.fillna('') # type: ignore

        return attack_table


    def make_weapon_attack_stat_table(self) -> pd.DataFrame:

        weapon_attack_table = pd.read_csv(f'{INPUTS_DIR}/weapon_attacks.csv', keep_default_na=False, index_col='Name') # type: ignore

        weapon_attack_table.drop(index='', inplace=True)
        weapon_attack_table.dropna(how='all', inplace=True) # type: ignore
        weapon_attack_table = weapon_attack_table.fillna('') # type: ignore

        return weapon_attack_table


class AttackStatDictionaryProvider:

    def __init__(self):
        attack_dataframe_factory = AttackCSVToDataFrameParser()
        self.weapon_attacks = attack_dataframe_factory.make_weapon_attack_stat_table()
        self.raw_attacks = attack_dataframe_factory.make_raw_attack_stat_table()

    def get_weapon_attack_stats_dict(self, attack_name: str):
        # Make a dictionary of the stats for the attack
        return self.weapon_attacks.loc[str(attack_name)].to_dict()

    def get_raw_attack_stats_dict(self, attack_name: str):
        # Make a dictionary of the stats for the attack
        return self.raw_attacks.loc[str(attack_name)].to_dict()

