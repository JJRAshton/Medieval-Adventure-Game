import random as rd
from typing import Dict, List

from ..npc import NPC
from ..player import Player
from ..map_object import Object
from ..classes import player_class
from ..attack import Attack
from ..item import Armour
from .attack_factory import AttackFactory
from .weapon_factory import WeaponFactory
from ....utils import dice_utils
from ...id_generator import IDGenerator

from .make_dataframes import ENTITY_STAT_PROVIDER, EntityStatDictionaryProvider, AttackStatDictionaryProvider
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

SIZE_FOR_STRING: Dict[str, int] = {
    'small': 5,
    'medium': 5,
    'large': 10,
    'huge':15,
    'gargantuan': 20
}

''' Factory for armour, objects, characters and players. '''
class EntityFactory:

    def __init__(self, id_generator: IDGenerator, map_number: int=1):
        self.character_stat_provider = CharacterStatDictionaryProvider(map_number)
        self.__id_generator: IDGenerator = id_generator
        self.__attack_factory = AttackFactory(AttackStatDictionaryProvider())
        self.__weapon_factory = WeaponFactory(self.__attack_factory, id_generator)

    # Returns a dictionary of stats for the given character
    def __getCharacterDict(self, character_name: str):
        return self.character_stat_provider.get_character_stats_dict(character_name)

    def create_object(self, object_name: str) -> Object:
        # Hmm, this is a bit suspicious
        obj_dict = self.__getArmourDict(object_name)
        new_object = Object(object_name, self.__id_generator.get_object_id(), int(obj_dict['Health']))

        new_object.armour['piercing'] = int(obj_dict['AC'])
        new_object.armour['slashing'] = int(obj_dict['AC'])
        new_object.armour['bludgeoning'] = int(obj_dict['AC'])

        is_inv = bool(obj_dict['Inventory'])

        if is_inv:
            new_object.inventory = []
        
        new_object.reset_health()

        return new_object

    # Adds the stats to the given player
    def create_player(self, preferences: Dict[str, str]={}) -> Player:
        if "name" in preferences and preferences["name"]:
            player_name = preferences["name"]
        else:
            player_name = rd.choice(Player.names)

        if "class" in preferences and preferences["class"]:
            selected_class = player_class.for_name(preferences["class"])
        else:
            selected_class = rd.choice(player_class.ALL)
        

        base_stats = {stat_name: stat for stat_name, stat in zip(selected_class.stat_order, sorted(dice_utils.roll_stats(), reverse=True))}
        
        df = ENTITY_STAT_PROVIDER.weapons
        if "weapon" in preferences and preferences["weapon"]:
            # The user could provide anything, but sanitisation is effort
            weapon_str = preferences["weapon"]
        else:
            # Not restricting weapon tier for now
            weapon_str = rd.choice(df[(df.Type.isin(selected_class.weapons))].index.tolist())

        equipped_weapons = {location: None for location in ['Left', 'Right', 'Both']}
        if df.loc[weapon_str].to_dict()['Two-handed']:
            equipped_weapons['Both'] = self.__weapon_factory.create(weapon_str)
        else:
            equipped_weapons['Right'] = self.__weapon_factory.create(weapon_str)

        player = Player(
            selected_class,
            weapon_factory=self.__weapon_factory,
            player_name=player_name,
            id=self.__id_generator.get_character_id(),
            base_attacks=self.__convert_attacks(['hit']),
            base_stats=base_stats,
            equipped_weapons=equipped_weapons,
        )

        return player

    def create_npc(self, npc_name: str, team=1) -> NPC:
        npc_stats = self.__getCharacterDict(npc_name)
        equipped_weapons = {location: None for location in ['Left', 'Right', 'Both']}
        for location in equipped_weapons.keys():
            if npc_stats[location]:
                equipped_weapons[location] = self.__weapon_factory.create(npc_stats[location])
        npc = NPC(
            npc_name,
            id=self.__id_generator.get_character_id(),
            base_attacks=self.__convert_attacks(dice_utils.convertList(npc_stats['Attacks'])),
            base_stats={stat: int(npc_stats[stat]) for stat in STATS},
            equipped_weapons=equipped_weapons,
            equipped_armour=self.__get_npc_armour(npc_stats['Armour Level']),
            vulnerabilities=dice_utils.safe_convert(npc_stats['Vulnerabilities']),
            resistances=dice_utils.safe_convert(npc_stats['Resistances']),
            base_movement=int(npc_stats['Speed']),
            team=team,
            size=SIZE_FOR_STRING[npc_stats['Size']],
            drop_rate=int(npc_stats['Drop Rate']),
            actions_total=int(npc_stats['Actions']),
            base_armour=int(npc_stats['Base Armour']),
            inventory=[], # dice_utils.convertList(char_dict['Inventory']) # The items actually need to be converted, ughh
            difficulty=int(npc_stats['Difficulty']),
            skill=int(npc_stats['Skill']) if npc_stats['Skill'] else 0
        )
        return npc

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

    
