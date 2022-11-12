import pandas as pd

char_in_dir = '../../resources/inputs/characters'
weapon_in_dir = '../../resources/inputs/weapons'

def read_char_inputs(character):
    character_df = pd.read_csv(f"{char_in_dir}/{character}.csv", header=None).transpose()
    character_df = character_df.rename(columns=character_df.iloc[0]).drop(character_df.index[0])
    character_df.set_index('Name', inplace=True)
    return character_df

def read_weapon_inputs(weapon):
    weapon_df = pd.read_csv(f"{weapon_in_dir}/{weapon}.csv", header=None).transpose()
    weapon_df = weapon_df.rename(columns=weapon_df.iloc[0]).drop(weapon_df.index[0])
    weapon_df.set_index('Name', inplace=True)
    return weapon_df

def make_stat_tables():
    # assign some useful variables

    # read combat setup
    df = pd.read_csv('../../resources/combat_setup.csv', keep_default_na=False)
    player_list = [x for x in df['Players'] if x != '']
    enemy_list = [x for x in df['Enemies'] if x != '']
    map_name = df['Map'].values[0]

    # construct dataframes of characters and weapons in this game - reference these tables to initialise things
    character_table = pd.DataFrame()
    for character in set(player_list + enemy_list):
        character_table = pd.concat([character_table, read_char_inputs(character)])

    weapons_list = character_table.loc[:, 'Weapon'].values.tolist()
    weapon_table = pd.DataFrame()
    for weapon in set(weapons_list):
        weapon_table = pd.concat([weapon_table, read_weapon_inputs(weapon)])

    return character_table, weapon_table

# make sets of all potential weapon and character parameters
all_weapon_params = {
    'weapon_id',
    'name',
    'type',
    'range',
    'dmg_dice',
    'dice_number',
    'is_finesse',
    'is_light',
    'is_heavy',
    'is_versatile',
}

all_character_params = {
    'character_id',
    'name',
    'size',
    'health',
    'ac',
    'attack_bonus',
    'weapon_name',
}
def get_weapon_stats_dict(weapon_name, weapon_table):
    # Make a dictionary of the stats for the entity
    gotten_stats = weapon_table.loc[str(weapon_name)].to_dict()
    return gotten_stats

def get_character_stats_dict(character_name, character_table):
    # Make a dictionary of the stats for the entity
    gotten_stats = character_table.loc[str(character_name)].to_dict()
    return gotten_stats

if __name__ == "__main__":
    character_table, weapon_table = make_stat_tables()

# print('game')