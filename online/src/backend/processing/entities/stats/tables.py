import pandas as pd
import os


inputs_dir = os.path.dirname(__file__) + '/../../../../../resources/inputs'

char_in_dir = f'{inputs_dir}/characters.csv'
player_in_dir = f'{inputs_dir}/players.csv'
weapon_in_dir = f'{inputs_dir}/weapons.csv'
armour_in_dir = f'{inputs_dir}/armour.csv'


def read_char_inputs():
    character_df = pd.read_csv(char_in_dir, header=None)
    character_df = character_df.rename(columns=character_df.iloc[0]).drop(character_df.index[0])
    character_df.set_index('Name', inplace=True)
    return character_df


def read_armour_inputs():
    armour_df = pd.read_csv(armour_in_dir, header=None)
    armour_df = armour_df.rename(columns=armour_df.iloc[0]).drop(armour_df.index[0])
    armour_df.set_index('Name', inplace=True)
    return armour_df


def read_weapon_inputs():
    weapon_df = pd.read_csv(weapon_in_dir, header=None)
    weapon_df = weapon_df.rename(columns=weapon_df.iloc[0]).drop(weapon_df.index[0])
    weapon_df.set_index('Name', inplace=True)
    return weapon_df


def make_character_stat_table(map_number_str):
    # assign some useful variables

    # read combat setup
    df = pd.read_csv(f'{inputs_dir}/maps/map{map_number_str}/entities.csv', keep_default_na=False)
    monster_list = [x for x in df['Monsters'] if x != '']
    npc_list = [x for x in df['NPCs'] if x != '']

    char_df = read_char_inputs()

    # construct dataframes of characters in this game - reference these tables to initialise things
    character_table = pd.DataFrame()
    for character in set(monster_list + npc_list):
        character_table = pd.concat([character_table, char_df])

    return character_table

def make_player_stat_table():
    # read combat setup
    player_table = pd.read_csv(f'{inputs_dir}/players.csv', keep_default_na=False, index_col='Entry')

    return player_table

def make_weapon_stat_table():
    # read combat setup
    weapon_table = pd.read_csv(f'{inputs_dir}/weapons.csv', keep_default_na=False, index_col='Name')

    return weapon_table

def make_armour_stat_table():
    # read combat setup
    armour_table = pd.read_csv(f'{inputs_dir}/armour.csv', keep_default_na=False, index_col='Name')

    return armour_table

def make_object_stat_table():
    # read combat setup
    armour_table = pd.read_csv(f'{inputs_dir}/objects.csv', keep_default_na=False, index_col='Name')

    return armour_table

class Tables:

    def __init__(self, mapNumber):
        self.map = str(mapNumber)
        self.characters = make_character_stat_table(self.map)
        self.armour = make_armour_stat_table()
        self.weapons = make_weapon_stat_table()
        self.players = make_player_stat_table()
        self.objects = make_object_stat_table()

    def get_weapon_stats_dict(self, weapon_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.weapons.loc[str(weapon_name)].to_dict()
        return gotten_stats

    def get_object_stats_dict(self, object_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.objects.loc[str(object_name)].to_dict()
        return gotten_stats

    def get_character_stats_dict(self, character_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.characters.loc[str(character_name)].to_dict()
        return gotten_stats

    def get_player_stats_dict(self, player_number):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.players.loc[player_number].to_dict()
        return gotten_stats

    def get_armour_stats_dict(self, armour_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.armour.loc[str(armour_name)].to_dict()
        return gotten_stats

