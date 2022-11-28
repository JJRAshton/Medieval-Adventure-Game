import pandas as pd
import os


inputs_dir = os.path.dirname(__file__) + '/../../../../../resources/inputs'

char_in_dir = f'{inputs_dir}/characters.csv'
player_in_dir = f'{inputs_dir}/players.csv'
weapon_in_dir = f'{inputs_dir}/weapons.csv'
armour_in_dir = f'{inputs_dir}/armour.csv'

weapon_types = ['axes', 'clubs', 'hammers',
                'bows', 'crossbows', 'light_throwables', 'heavy_throwables',
                'shields', 'single_edged_swords', 'double_edged_swords', 'edgeless_swords',
                'glaives', 'polearms', 'spears',
                'special',  'mythical',
                'staves', 'books']


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

    all_char_df = read_char_inputs()
    all_char_df.dropna(how='all', inplace=True)

    # construct dataframes of characters in this game - reference these tables to initialise things
    character_table = all_char_df.loc[list(set(monster_list + npc_list))]

    character_table = character_table.fillna('')

    return character_table


def make_weapon_stat_table():

    weapon_table = pd.DataFrame()
    for weapon_type in weapon_types:
        weapon_type_table = pd.read_csv(f'{inputs_dir}/weapons/{weapon_type}.csv', keep_default_na=False, index_col='Name')
        types = [weapon_type for _ in range(weapon_type_table.shape[0])]
        weapon_type_table['Type'] = types
        weapon_table = pd.concat([weapon_table, weapon_type_table])

        weapon_table = weapon_table.fillna('')

    return weapon_table


def make_armour_stat_table():
    # read combat setup
    armour_table = pd.read_csv(f'{inputs_dir}/armour.csv', keep_default_na=False, index_col='Name')

    return armour_table


def make_object_stat_table():
    # read combat setup
    armour_table = pd.read_csv(f'{inputs_dir}/objects.csv', keep_default_na=False, index_col='Name')

    return armour_table


class EntityTables:

    def __init__(self, mapNumber):
        self.map = str(mapNumber)
        self.characters = make_character_stat_table(self.map)
        self.armour = make_armour_stat_table()
        self.objects = make_object_stat_table()
        self.weapons = make_weapon_stat_table()

    def get_weapon_stats_dict(self, weapon_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.weapons.loc[weapon_name].to_dict()
        return gotten_stats

    def get_object_stats_dict(self, object_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.objects.loc[object_name].to_dict()
        return gotten_stats

    def get_character_stats_dict(self, character_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.characters.loc[character_name].to_dict()
        return gotten_stats

    def get_armour_stats_dict(self, armour_name):
        # Make a dictionary of the stats for the entity
        gotten_stats = self.armour.loc[armour_name].to_dict()
        return gotten_stats


def make_raw_attack_stat_table():

    attack_table = pd.read_csv(f'{inputs_dir}/raw_attacks.csv', keep_default_na=False, index_col='Name')

    attack_table.dropna(how='all', inplace=True)
    attack_table = attack_table.fillna('')

    return attack_table


def make_weapon_attack_stat_table():

    weapon_attack_table = pd.read_csv(f'{inputs_dir}/weapon_attacks.csv', keep_default_na=False, index_col='Name')

    weapon_attack_table.drop(index='', inplace=True)
    weapon_attack_table.dropna(how='all', inplace=True)
    weapon_attack_table = weapon_attack_table.fillna('')

    return weapon_attack_table


class AttackTables:

    def __init__(self):
        self.weapon_attacks = make_weapon_attack_stat_table()
        self.raw_attacks = make_raw_attack_stat_table()

    def get_weapon_attack_stats_dict(self, attack_name):
        # Make a dictionary of the stats for the attack
        gotten_stats = self.weapon_attacks.loc[str(attack_name)].to_dict()
        return gotten_stats

    def get_raw_attack_stats_dict(self, attack_name):
        # Make a dictionary of the stats for the attack
        gotten_stats = self.raw_attacks.loc[str(attack_name)].to_dict()
        return gotten_stats

