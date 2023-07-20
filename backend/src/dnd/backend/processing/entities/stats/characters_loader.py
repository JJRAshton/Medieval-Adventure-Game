from typing import Dict, List
import pandas as pd
import os

INPUTS_DIR = os.path.dirname(__file__) + '/../../../../../../resources/inputs'


class CharacterCSVToDataFrameParser():

    def __parse_csv(self, directory: str):
        data_frame: pd.DataFrame = pd.read_csv(directory, header=None) # type: ignore
        data_frame = data_frame.rename(columns=data_frame.iloc[0]).drop(data_frame.index[0]) # type: ignore
        data_frame.set_index('Name', inplace=True) # type: ignore
        return data_frame

    def make_character_stat_table(self, map_number_str: str):
        # It looks like there's two distinct things going on here:
        #   - Reading the map specific entities.csv to see what characters should be present
        #   - Reading the general characters.csv to get stats for particular characters
        #
        # It would be nice to split these up, and probably put the static characters.csv
        # reading in ./make_datafromes.py
        df: pd.DataFrame = pd.read_csv(f'{INPUTS_DIR}/maps/map{map_number_str}/entities.csv', keep_default_na=False) # type: ignore
        monster_list: List[str] = [x for x in df['Monsters'] if x != '']
        npc_list: List[str] = [x for x in df['NPCs'] if x != '']

        all_char_df = self.__parse_csv(f'{INPUTS_DIR}/characters.csv')
        all_char_df.dropna(how='all', inplace=True) # type: ignore

        # construct dataframes of characters in this game - reference these tables to initialise things
        character_table = all_char_df.loc[list(set(monster_list + npc_list))]

        character_table = character_table.fillna('') # type: ignore

        return character_table


class CharacterStatDictionaryProvider:

    def __init__(self, map_number: int):
        ''' Provides dictionaries containing stats for characters only '''
        self.map = str(map_number)
        data_frame_factory = CharacterCSVToDataFrameParser()
        self.__characters = data_frame_factory.make_character_stat_table(self.map)

    def get_character_stats_dict(self, character_name: str) -> Dict[str, object]:
        # Make a dictionary of the stats for the entity
        gotten_stats: Dict[str, object] = self.__characters.loc[character_name].to_dict() # type: ignore
        return gotten_stats
