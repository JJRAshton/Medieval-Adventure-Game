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

    def __parse_csv(self, directory: str):
        data_frame: pd.DataFrame = pd.read_csv(directory, header=None) # type: ignore
        data_frame = data_frame.rename(columns=data_frame.iloc[0]).drop(data_frame.index[0]) # type: ignore
        data_frame.set_index('Name', inplace=True) # type: ignore
        return data_frame

    def make_character_stat_table(self, map_number_str: str):
        # assign some useful variables

        # read combat setup
        df: pd.DataFrame = pd.read_csv(f'{INPUTS_DIR}/maps/map{map_number_str}/entities.csv', keep_default_na=False) # type: ignore
        monster_list: List[str] = [x for x in df['Monsters'] if x != '']
        npc_list: List[str] = [x for x in df['NPCs'] if x != '']

        all_char_df = self.__parse_csv(f'{INPUTS_DIR}/characters.csv')
        all_char_df.dropna(how='all', inplace=True) # type: ignore

        # construct dataframes of characters in this game - reference these tables to initialise things
        character_table = all_char_df.loc[list(set(monster_list + npc_list))]

        character_table = character_table.fillna('') # type: ignore

        return character_table
    

    def make_weapon_stat_table(self):
        weapon_table = pd.DataFrame()
        for weapon_type in weapon_types:
            weapon_type_table = pd.read_csv(f'{INPUTS_DIR}/weapons/{weapon_type}.csv', keep_default_na=False, index_col='Name') # type: ignore
            types = [weapon_type for _ in range(weapon_type_table.shape[0])]
            weapon_type_table['Type'] = types
            weapon_table = pd.concat([weapon_table, weapon_type_table]) # type: ignore

            weapon_table = weapon_table.fillna('') # type: ignore

        return weapon_table


    def make_armour_stat_table(self):
        # read combat setup
        armour_table = pd.read_csv(f'{INPUTS_DIR}/armour.csv', keep_default_na=False, index_col='Name') # type: ignore

        return armour_table


    def make_object_stat_table(self): # Unused?
        # read combat setup
        armour_table = pd.read_csv(f'{INPUTS_DIR}/objects.csv', keep_default_na=False, index_col='Name') # type: ignore

        return armour_table


class EntityStatDictionaryProvider:

    def __init__(self, mapNumber: int):
        ''' Provides dictionaries containing stats for "Entities" (everything
        except attacks and weapons?) '''
        self.map = str(mapNumber)
        data_frame_factory = EntityCSVToDataFrameParser()
        self.__characters = data_frame_factory.make_character_stat_table(self.map)
        self.__armour = data_frame_factory.make_armour_stat_table()
        self.__objects = data_frame_factory.make_object_stat_table()
        self.weapons = data_frame_factory.make_weapon_stat_table()

    def get_weapon_stats_dict(self, weapon_name: str) -> Dict[str, str]:
        # Make a dictionary of the stats for the entity
        gotten_stats: Dict[str, str] = self.weapons.loc[weapon_name].to_dict() # type: ignore
        return gotten_stats

    def get_character_stats_dict(self, character_name: str) -> Dict[str, object]:
        # Make a dictionary of the stats for the entity
        gotten_stats: Dict[str, object] = self.__characters.loc[character_name].to_dict() # type: ignore
        return gotten_stats

    def get_armour_stats_dict(self, armour_name: str) -> Dict[str, str]:
        # Make a dictionary of the stats for the entity
        gotten_stats: Dict[str, str] = self.__armour.loc[armour_name].to_dict() # type: ignore
        return gotten_stats


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
        gotten_stats = self.weapon_attacks.loc[str(attack_name)].to_dict()
        return gotten_stats

    def get_raw_attack_stats_dict(self, attack_name: str):
        # Make a dictionary of the stats for the attack
        gotten_stats = self.raw_attacks.loc[str(attack_name)].to_dict()
        return gotten_stats

