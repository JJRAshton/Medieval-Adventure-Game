import random as rd
from typing import Dict, List

from ..npc import NPC
from ..npc import Monster
from ..player import Player
from ..map_object import Object
from ..classes import player_class
from ..attack import Attack
from ..item import Armour
from .attack_factory import AttackFactory
from .weapon_factory import WeaponFactory
from ....utils import dice_utils

from .make_dataframes import EntityStatDictionaryProvider, AttackStatDictionaryProvider
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
        self.__attack_factory = AttackFactory(AttackStatDictionaryProvider())
        self.__weapon_factory = WeaponFactory(EntityStatDictionaryProvider(), self.__attack_factory)

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
    def get_character_stats(self, character: NPC, char_dict):
        size = char_dict['Size']

        if char_dict['Base Armour']:
            character.base_armour = int(char_dict['Base Armour'])
            character.base_coverage = 1
        if char_dict['Inventory']:
            inventory = dice_utils.convertList(char_dict['Inventory'])
            # These need to be converted to items instead of strings but
            # it would be a pain working out what they should be
            character.inventory = [] # character.inventory = inventory

        character.actions_total = int(char_dict['Actions'])
        character.drop_rate = int(char_dict['Drop Rate'])
        character.skill = int(char_dict['Skill']) if char_dict['Skill'] else 0
        character.difficulty = int(char_dict['Difficulty'])

        character.base_evasion = character.base_stat['DEX']

        character.baseHealth = dice_utils.roll_dice(int(char_dict['Difficulty']), character.base_stat['CON'], character.base_stat['CON'])
        if size == 'large':
            character.size = 10
        elif size == 'huge':
            character.size = 15
        elif size == 'gargantuan':
            character.size = 20
        else:
            character.size = 5

        character.base_reach = character.size

    # Adds the stats to the given player
    def create_player(self, player_class: player_class.PlayerClass, player_name=None) -> Player:
        if player_name is None:
            player_name = rd.choice(Player.names)
        base_stats = {stat_name: stat for stat_name, stat in zip(player_class.stat_order, sorted(dice_utils.roll_stats(), reverse=True))}
        
        df = self.stat_provider.weapons
        weapon_str = rd.choice(df[(df.Type.isin(player_class.weapons)) & (df.Tier == 4)].index.tolist())

        equipped_weapons = {location: None for location in ['Left', 'Right', 'Both']}
        if df.loc[weapon_str].to_dict()['Two-handed']:
            equipped_weapons['Both'] = self.__weapon_factory.create(weapon_str)
        else:
            equipped_weapons['Right'] = self.__weapon_factory.create(weapon_str)

        player = Player(
            player_class,
            weapon_factory=self.__weapon_factory,
            player_name=player_name,
            base_attacks=self.__convert_attacks(['hit']),
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
        )

        player.behaviour_type = 1
        player.team = 1

        return player

    def create_npc(self, npc_name: str) -> NPC:
        npc_stats = self.__getCharacterDict(npc_name)
        equipped_weapons = {location: None for location in ['Left', 'Right', 'Both']}
        for location in equipped_weapons.keys():
            if npc_stats[location]:
                equipped_weapons[location] = self.__weapon_factory.create(npc_stats[location])
        npc = NPC(
            npc_name,
            base_attacks=self.__convert_attacks(dice_utils.convertList(npc_stats['Attacks'])),
            base_stats={stat: int(npc_stats[stat]) for stat in STATS},
            equipped_weapons=equipped_weapons,
            equipped_armour=self.__get_npc_armour(npc_stats['Armour Level']),
            vulnerabilities=dice_utils.safe_convert(npc_stats['Vulnerabilities']),
            resistances=dice_utils.safe_convert(npc_stats['Resistances']),
            base_movement=int(npc_stats['Speed'])
        )
        self.get_character_stats(npc, npc_stats)
        npc.setup() # Should be moved into constructor once get_character_stats is removed
        return npc

    def create_monster(self, monster_name: str) -> Monster:
        monster_stats = self.__getCharacterDict(monster_name)
        equipped_weapons = {location: None for location in ['Left', 'Right', 'Both']}
        for location in equipped_weapons.keys():
            if monster_stats[location]:
                equipped_weapons[location] = self.__weapon_factory.create(monster_stats[location])
        monster = Monster(
            monster_name,
            base_attacks=self.__convert_attacks(dice_utils.convertList(monster_stats['Attacks'])),
            base_stats={stat: int(monster_stats[stat]) for stat in STATS},
            equipped_weapons=equipped_weapons,
            equipped_armour=self.__get_npc_armour(monster_stats['Armour Level']),
            vulnerabilities=dice_utils.safe_convert(monster_stats['Vulnerabilities']),
            resistances=dice_utils.safe_convert(monster_stats['Resistances']),
            base_movement=int(monster_stats['Speed'])
        )
        self.get_character_stats(monster, monster_stats)
        monster.setup() # Should be moved into constructor once get_character_stats is removed
        return monster


    def __convert_attacks(self, attack_strings: List[str]) -> List[Attack]:
        base_attacks = []
        for i, attack_str in enumerate(attack_strings):
            attack = self.__attack_factory.create(attack_str)
            attack.id = i
            base_attacks.append(attack)
        return base_attacks
    
    def __get_npc_armour(self, armour_string) -> Dict[str, Armour | None]:
        # Randomly selects armour according to armour level
        equipped_armour = {'Under': None, 'Over': None}
        if armour_string:
            level = int(armour_string)

            if level > 2:
                for armour_type in armour_levels[level]:
                    armour_list = armour_levels[level][armour_type]
                    armour = rd.choice(armour_list)
                    equipped_armour[armour_type] = self.__weapon_factory.create_armour(armour)
                    if armour == 'padded_jack':
                        break
            else:
                armour_list = armour_levels[level]
                equipped_armour['Under'] = self.__weapon_factory.create_armour(rd.choice(armour_list))
        return equipped_armour

    
