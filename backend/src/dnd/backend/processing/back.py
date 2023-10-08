import pickle as pkl
import random as rd
from typing import Dict, List, Set, Tuple
import pandas as pd
import os

from ...api.users import User

from .entities.item import Weapon, Armour

from .entities.stats.entity_factory import EntityFactory

from .entities.health_entity import HealthEntity
from .entities.character import Character
from .entities.classes import player_class
from .entities.map_object import Object
from .id_generator import IDGenerator, is_character


# Gets the in game distance between two coords for travel
def calcPathDist(coords1: Tuple[int, int], coords2: Tuple[int, int]) -> int:
    return 5 * max(abs(coords2[0] - coords1[0]), abs(coords2[1] - coords1[1]))

def load_pkl(file_name):
    with open(file_name, 'rb') as f:
        contents = pkl.load(f)
    return contents

class Back:
    maps_dir = os.path.dirname(__file__) + '/../../../../resources/inputs/maps'

    def __init__(self, map_no: int or str, users: Set[User], builtin_map: int, id_generator: IDGenerator,  classes: List[str] = []):
        if builtin_map:
            self.map_path = f'{Back.maps_dir}/map{map_no}'
        else:
            self.map_path = map_no

        self.__entity_factory = EntityFactory(id_generator, map_no)
        self.id_generator: IDGenerator = id_generator

        self.terrainGrid = load_pkl(f'{self.map_path}/terrain.pkl')
        self.size = (len(self.terrainGrid), len(self.terrainGrid[0]))

        self.characterGrid = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.itemGrid = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.spawn = {
            'Player': load_pkl(f'{self.map_path}/player_spawn.pkl'),
            'Monster': load_pkl(f'{self.map_path}/monster_spawn.pkl'),
            'NPC': load_pkl(f'{self.map_path}/npc_spawn.pkl')
        }

        self.entities: Dict[str, HealthEntity] = {}  # All entities in dictionary with ids as keys

        self.items = []
        self.weapons = []
        self.armour = []

        self.characters: Dict[str, HealthEntity] = {}

        if not classes:
            classes = [player_class.RAIDER, player_class.GLADIATOR, player_class.GUARDIAN, player_class.KNIGHT, player_class.SAMURAI]
        self.classes = classes  # For choosing the class from backend - before frontend input

        self.objects = []
        self.objectGrid = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]
        with open(f'{self.map_path}/objects.pkl', 'rb') as object_file:
            objectList = pkl.load(object_file)
        for object_info in objectList:
            name, coords = object_info
            i_object: Object = self.__entity_factory.create_object(name)
            self.objectGrid[coords[0]][coords[1]] = i_object
            self.objects.append(i_object)
            self.entities[i_object.id] = i_object

        df: pd.DataFrame = pd.read_csv(f'{self.map_path}/entities.csv', keep_default_na=False) # type: ignore
        monster_list: List[str] = [x for x in df['Monsters'] if x != ''] # type: ignore
        self.monsters: List[HealthEntity] = [self.createCharacter('Monster', monster) for monster in monster_list]

        npc_list: List[str] = [x for x in df['NPCs'] if x != ''] # type: ignore
        self.npcs: List[HealthEntity] = [self.createCharacter('NPC', npc) for npc in npc_list]  # Non-monsters

        self.players = []
        for user in users:
            next_character = self.createCharacter('Player', preferences={
                "name": user.player_name,
                "class": user.player_class,
                "weapon": user.player_weapon
            })
            self.players.append(next_character)
            user.character_id = next_character.id

    # Creates and registers a character and its inventory
    def createCharacter(self, character_type: str, sub_type: str | None=None, preferences: Dict[str, str]={}) -> HealthEntity:
        if character_type == 'Player' and sub_type is None:
            character: HealthEntity = self.__entity_factory.create_player(preferences)
        elif character_type == 'Monster' and sub_type is not None:
            character: HealthEntity = self.__entity_factory.create_npc(sub_type, team=2)
        elif character_type == 'NPC' and sub_type is not None:
            character: HealthEntity = self.__entity_factory.create_npc(sub_type, team=1)
        else:
            raise ValueError

        self.characters[character.id] = character
        self.entities[character.id] = character

        for item in list(character.equipped_weapons.values()) + list(character.equipped_armour.values()) + character.inventory:
            if item is not None:
                self.items.append(item)
                if isinstance(item, Armour):
                    self.armour.append(item)
                elif isinstance(item, Weapon):
                    self.weapons.append(item)

        rand_index = rd.randint(0, len(self.spawn[character_type])-1)
        spawn_coords = self.spawn[character_type].pop(rand_index)

        character.coords = spawn_coords
        self.characterGrid[spawn_coords[0]][spawn_coords[1]] = character
        character.initialiseTurn()

        return character

    # Moves a character on the grid
    def moveCharacter(self, charID: str, newCoords: Tuple[int, int]):
        character = self.entities[charID]
        prevCoords = character.coords
        vector = (newCoords[0]-prevCoords[0], newCoords[1]-prevCoords[1])

        character.move(vector)

        self.characterGrid[newCoords[0]][newCoords[1]] = character
        self.characterGrid[prevCoords[0]][prevCoords[1]] = None

        if self.is_item(newCoords):
            item = self.itemGrid[newCoords[0]][newCoords[1]]
            item.is_carried = True

            self.itemGrid[newCoords[0]][newCoords[1]] = None
            character.inventory.append(item)

    # Moves an object on the grid
    def moveObject(self, objID: str, newCoords: Tuple[int, int]):
        entity = self.entities[objID]
        prevCoords = entity.coords
        vector = (newCoords[0]-prevCoords[0], newCoords[1]-prevCoords[1])

        entity.move(vector)

        self.objectGrid[newCoords[0]][newCoords[1]] = entity
        self.objectGrid[prevCoords[0]][prevCoords[1]] = None

    # Drops an item from an inventory
    def dropInv(self, character: Character):
        inv_length = len(character.inventory)
        if inv_length > 0:
            index = rd.randint(0, inv_length-1)
            item = character.inventory.pop(index)

            item.coords = character.coords
            self.itemGrid[item.coords[0]][item.coords[1]] = item

            item.is_carried = False

    # Moves the character along the given path to the given index
    def pathCharacter(self, charID: int, pathCoords: List[Tuple[int, int]], index: int):  # For now, just moves to the final allowed coord
        if index != -1:
            finalCoord = pathCoords[index]

            self.moveCharacter(charID, finalCoord)
            return True
        else:
            return False

    # Checks if there is an item at the given coords
    def is_item(self, coords: Tuple[int, int]):
        return self.itemGrid[coords[0]][coords[1]] is not None

    # Checks if there is a character at the given coords
    def is_character(self, coords: Tuple[int, int]):
        return self.characterGrid[coords[0]][coords[1]] is not None

    # Checks if there is an object at the given coords
    def is_object(self, coords: Tuple[int, int]):
        return self.objectGrid[coords[0]][coords[1]] is not None

    # Checks if coords are valid to move to
    def is_validCoords(self, newCoords: Tuple[int, int]):
        x, y = newCoords
        size = (len(self.characterGrid[0]), len(self.characterGrid))

        is_occupied: bool = self.is_character(newCoords) or self.is_object(newCoords)
        return 0 <= x <= size[0] and 0 <= y <= size[1] and not is_occupied

    # Checks if character has the movement to move to coords
    def is_validMovement(self, charID: str, newCoords: Tuple[int, int]):
        x, y = newCoords
        oldx, oldy = self.entities[charID].coords
        return self.entities[charID].movement >= calcPathDist((oldx, oldy), (x, y))

    # Checks if the character can move along the given path
    def is_validPath(self, charID: str, pathCoords: Tuple[int, int]):
        character = self.entities[charID]
        remaining_movement = character.movement

        index = -1
        for coord in pathCoords:
            if remaining_movement == 0 or not self.is_validCoords(coord):
                break
            remaining_movement -= 5
            index += 1

        return index

    # Checks if an attack is valid
    def is_validAttack(self, atkID: int, defID: int) -> bool:
        in_range: bool = calcPathDist(self.entities[atkID].coords, self.entities[defID].coords) <= self.entities[atkID].reach
        has_attacks: bool = is_character(atkID) and self.entities[atkID].actions > 0

        return in_range and has_attacks
