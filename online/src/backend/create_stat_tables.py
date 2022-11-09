import pandas as pd

# assign some useful variables
char_in_dir = '../inputs/characters'
weapon_in_dir = '../inputs/weapons'

# read combat setup
df = pd.read_csv('../combat_setup.csv', keep_default_na=False)
player_list = [x for x in df['Players'] if x != '']
enemy_list = [x for x in df['Enemies'] if x != '']
map_name = df['Map'].values[0]

# construct dataframes of weapons and characters - reference these tables to initialise objects
def read_char_inputs(character):
    character_df = pd.read_csv(f"{char_in_dir}/{character}.csv", header=None).transpose()
    character_df = character_df.rename(columns=character_df.iloc[0]).drop(character_df.index[0])
    return character_df

def read_weapon_inputs(weapon):
    weapon_df = pd.read_csv(f"{weapon_in_dir}/{weapon}.csv", header=None).transpose()
    weapon_df = weapon_df.rename(columns=weapon_df.iloc[0]).drop(weapon_df.index[0])
    return weapon_df

weapons_list = ['greataxe', 'greatsword']
weapon_table = pd.DataFrame()
for weapon in set(weapons_list):
    weapon_table = pd.concat([weapon_table, read_weapon_inputs(weapon)], ignore_index=True)

character_table = pd.DataFrame()
for character in set(player_list+enemy_list):
    character_table = pd.concat([character_table, read_char_inputs(character)], ignore_index=True)

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

print('game')