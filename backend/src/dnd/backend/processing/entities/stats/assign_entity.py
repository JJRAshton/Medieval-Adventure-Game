import random as rd
from typing import List
import pandas as pd

from ..npc import NPC
from ..npc import Monster
from ..player import Player
from ..item import Armour
from ..map_object import Object
from ..classes import player_class

from ....utils import dice_utils

from .make_dataframes import EntityStatDictionaryProvider
from .characters_loader import CharacterStatDictionaryProvider

STATS = ['STR', 'DEX', 'CON', 'WIT']

# Different armour levels for characters
armour_levels = {
    1: ['hide', 'leather'],
    2: ['hide', 'leather', 'padded_tunic', 'arming_doublet', 'gambeson'],
    3: {
        'Under': ['hide', 'leather'],
        'Over': ['hauberk', 'scale', 'splint', 'lamellar']
    },
    4: {
        'Under': ['leather', 'padded_tunic', 'arming_doublet', 'gambeson', 'padded_jack'],
        'Over':  ['breastplate', 'cuirass', 'hauberk', 'hauberk_riveted', 'scale', 'splint', 'lamellar']
    },
    5: {
        'Under': ['padded_tunic', 'arming_doublet'],
        'Over':  ['laminar', 'plate', 'full_plate']
    }
}

''' Factory for armour, objects, characters and players. '''
class EntityFactory:

    def __init__(self, map_number: int=1):
        self.stat_provider = EntityStatDictionaryProvider()
        self.character_stat_provider = CharacterStatDictionaryProvider(map_number)

    # Returns a dictionary of stats for the given character
    def __getCharacterDict(self, character_name: str):
        return self.character_stat_provider.get_character_stats_dict(character_name)

    def create_object(self, object_name: str) -> Object:
        new_object = Object(object_name)

        # Hmm, this is a bit suspicious
        obj_dict = self.__getArmourDict(object_name.name)

        new_object.armour['piercing'] = int(obj_dict['AC'])
        new_object.armour['slashing'] = int(obj_dict['AC'])
        new_object.armour['bludgeoning'] = int(obj_dict['AC'])
        new_object.baseHealth = int(obj_dict['Health'])

        is_inv = bool(obj_dict['Inventory'])

        if is_inv:
            new_object.inventory = []
        
        new_object.reset_health()

        return new_object

    # This should eventually just take a char_dict and provide a character back
    def get_character_stats(self, character, char_dict):  # Doesn't collect all data
        starting_items: List[object] = []

        size = char_dict['Size']

        for location in ['Left', 'Right', 'Both']:
            if char_dict[location]:
                character.equipped_weapons[location] = char_dict[location]
                starting_items.append(char_dict[location])

        if char_dict['Base Armour']:
            character.baseArmour = char_dict['Base Armour']
            character.base_coverage = 1
        if char_dict['Inventory']:
            inventory = dice_utils.convertList(char_dict['Inventory'])
            character.inventory = inventory
            starting_items += inventory
        if char_dict['Skill']:
            character.skill = int(char_dict['Skill'])

        character.starting_items = starting_items

        # Randomly selects armour according to armour level
        if char_dict['Armour Level']:
            level = int(char_dict['Armour Level'])

            if level > 2:
                for armour_type in armour_levels[level]:
                    armour_list = armour_levels[level][armour_type]
                    armour = rd.choice(armour_list)
                    character.armour[armour_type] = armour
                    if armour == 'padded_jack':
                        break
            else:
                armour_list = armour_levels[level]
                character.armour['Light'] = rd.choice(armour_list)

        if char_dict['Vulnerabilities']:
            vulnerabilities = dice_utils.convertList(char_dict['Vulnerabilities'])
            character.vulnerabilities += vulnerabilities
        if char_dict['Resistances']:
            resistances = dice_utils.convertList(char_dict['Resistances'])
            character.resistances += resistances

        character.actions_total = int(char_dict['Actions'])
        character.base_movement = int(char_dict['Speed'])
        character.drop_rate = int(char_dict['Drop Rate'])
        character.skill = int(char_dict['Skill']) if char_dict['Skill'] else 0
        character.difficulty = int(char_dict['Difficulty'])

        character.base_evasion = character.base_stat['DEX']
        
        character.baseHealth = dice_utils.roll_dice(int(char_dict['Difficulty']), character.base_stat['CON'], character.base_stat['CON'])
        if size == 'large':
            character.size = 10
            character.dmg_mult = 2
        elif size == 'huge':
            character.size = 15
            character.dmg_mult = 4
        elif size == 'gargantuan':
            character.size = 20
            character.dmg_mult = 8
        else:
            character.size = 5
            character.dmg_mult = 1

        character.base_reach = character.size

    # Adds the stats to the given player
    def create_player(self, player_class: player_class.PlayerClass, playerName=None) -> Player:
        if playerName is None:
            playerName = rd.choice(Player.names)
        base_stats = {stat_name: stat for stat_name, stat in zip(player_class.stat_order, sorted(self.roll_stats(), reverse=True))}
        player = Player(
            player_class,
            playerName,
            base_attacks=['hit'],
            base_stats=base_stats
        )
        
        player.chosen_weapons = []

        player.behaviour_type = 1
        player.team = 1

        df = self.stat_provider.weapons
        wep_option_df = pd.DataFrame()
        for wep_type in player_class.weapons:
            wepData = df[(df.Type == wep_type) & (df.Tier == 4)]
            wep_option_df = pd.concat([wep_option_df, wepData]) 

        choices = wep_option_df.index.tolist()

        weapon_str = rd.choice(choices)
        if df.loc[weapon_str].to_dict()['Two-handed']:
            player.equipped_weapons['Both'] = weapon_str
        else:
            player.equipped_weapons['Right'] = weapon_str

        player.convAttacks()

        player.getClass()
        player.getEquipment()

        player.resetStats()

        player.refreshStatAfterEquipment()
 
        player.calcHealth()

        player.reset_health()

        player.calcInitiative()

        player.reset_health()

        return player

    def roll_stats(self):
        x, n, top = 3, 8, 48  # roll 8, take best 5 - max of 40
        stat_rolls = []

        for _ in range(4):  # Number of stats to assign
            one_stat_roll = []
            for _ in range(n):  # Rolls n dice
                roll = rd.randint(1, int(top/x))
                one_stat_roll.append(roll)

            for _ in range(n-x):  # Get rid of the lowest values
                one_stat_roll.pop(one_stat_roll.index(min(one_stat_roll)))

            stat_rolls.append(sum(one_stat_roll))
        return stat_rolls

    def create_npc(self, npc_name: str) -> NPC:
        npc_stats = self.__getCharacterDict(npc_name)
        npc = NPC(
            npc_name,
            base_attacks=dice_utils.convertList(npc_stats['Attacks']),
            base_stats={stat: int(npc_stats[stat]) for stat in STATS}
        )
        self.get_character_stats(npc, npc_stats)
        self.setup_npc(npc)

        return npc

    def create_monster(self, monster_name: str) -> Monster:
        monster_stats = self.__getCharacterDict(monster_name)
        monster = Monster(
            monster_name,
            base_attacks=dice_utils.convertList(monster_stats['Attacks']),
            base_stats={stat: int(monster_stats[stat]) for stat in STATS}
        )
        self.get_character_stats(monster, monster_stats)
        self.setup_npc(monster)

        return monster
    
    def setup_npc(self, npc: NPC):
        npc.getEquipment()
        npc.convAttacks()

        npc.resetStats()
        npc.reset_health()

        npc.refreshStatAfterEquipment()
        npc.calcInitiative()

    
