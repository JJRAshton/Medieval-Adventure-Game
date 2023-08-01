import pickle as pkl
import random as rd
from typing import Dict, List, Tuple
import pandas as pd
import os

from .entities.stats.assign_entity import EntityFactory

from .entities.health_entity import HealthEntity
from .entities.character import Character
from .entities.classes import player_class
from .entities.map_object import Object


# Gets the in game distance between two coords for travel
def calcPathDist(coords1: Tuple[int, int], coords2: Tuple[int, int]) -> int:
    return 5 * max(abs(coords2[0] - coords1[0]), abs(coords2[1] - coords1[1]))


class Back:
    maps_dir = os.path.dirname(__file__) + '/../../../../resources/inputs/maps'

    def __init__(self, map_no: int or str, nPlayers: int, builtin_map: int, classes: List[str] = []):
        if builtin_map:
            self.map_path = f'{Back.maps_dir}/map{map_no}'
        else:
            self.map_path = map_no

        self.__entity_factory = EntityFactory(map_no)
        self.player_n = nPlayers
        self.size = (0, 0)

        self.terrainGrid = []

        self.characterGrid = []
        self.objectGrid = []
        self.itemGrid = []

        self.spawn = {}

        self.entities: Dict[int, HealthEntity] = {}  # All entities in dictionary with ids as keys

        self.objects = []

        self.items = []
        self.weapons = []
        self.armour = []

        self.characters: List[HealthEntity] = []
        self.players: List[HealthEntity] = []
        self.monsters: List[HealthEntity] = []
        self.npcs: List[HealthEntity] = []  # Non-monsters

        if not classes:
            classes = [player_class.RAIDER, player_class.GLADIATOR, player_class.GUARDIAN, player_class.KNIGHT, player_class.SAMURAI]
        self.classes = classes  # For choosing the class from backend - before frontend input

        self.loadMap()
        self.addMapNPCs()

        for _ in range(self.player_n):
            self.players.append(self.createCharacter('Player'))

    # Loads in the map from the map number given
    def loadMap(self):
        self.terrainGrid = pkl.load(open(f'{self.map_path}/terrain.pkl', 'rb'))
        self.size = (len(self.terrainGrid), len(self.terrainGrid[0]))

        self.characterGrid = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.itemGrid = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.objectGrid = [[None for _ in range(self.size[1])] for _ in range(self.size[0])]
        objectList = pkl.load(open(f'{self.map_path}/objects.pkl', 'rb'))
        for objectID, object_info in enumerate(objectList, start=100):
            name, coords = object_info
            i_object: Object = self.__entity_factory.create_object(name)
            i_object.id = objectID
            self.objectGrid[coords[0]][coords[1]] = i_object
            self.objects.append(i_object)
            self.entities[objectID] = i_object

        self.spawn = {
            'Player': pkl.load(open(f'{self.map_path}/player_spawn.pkl', 'rb')),
            'Monster': pkl.load(open(f'{self.map_path}/monster_spawn.pkl', 'rb')),
            'NPC': pkl.load(open(f'{self.map_path}/npc_spawn.pkl', 'rb'))
        }

    # Adds in the map NPCs
    def addMapNPCs(self):
        df: pd.DataFrame = pd.read_csv(f'{self.map_path}/entities.csv', keep_default_na=False) # type: ignore
        monster_list: List[str] = [x for x in df['Monsters'] if x != ''] # type: ignore
        npc_list: List[str] = [x for x in df['NPCs'] if x != ''] # type: ignore

        for monster_str in monster_list:
            self.monsters.append(self.createCharacter('Monster', monster_str))

        for npc_str in npc_list:
            self.npcs.append(self.createCharacter('NPC', npc_str))

    # Creates and registers a character and its inventory
    def createCharacter(self, character_type: str, sub_type: str | None=None) -> HealthEntity:
        if character_type == 'Player' and sub_type is None:
            character: HealthEntity = self.__entity_factory.create_player(self.classes.pop(0))
        elif character_type == 'Monster' and sub_type is not None:
            character: HealthEntity = self.__entity_factory.create_monster(sub_type)
        elif character_type == 'NPC' and sub_type is not None:
            character: HealthEntity = self.__entity_factory.create_npc(sub_type)
        else:
            raise ValueError

        charIDNum = len(self.characters)
        itemIDNum = len(self.items) + 200

        character.id = charIDNum
        self.characters.append(character)
        self.entities[charIDNum] = character

        for hand in character.equipped_weapons:
            if character.equipped_weapons[hand] is not None:
                character.equipped_weapons[hand].id = itemIDNum
                self.items.append(character.equipped_weapons[hand])
                self.weapons.append(character.equipped_weapons[hand])
                itemIDNum += 1
        for armour_type in character.equipped_armour:
            if character.equipped_armour[armour_type] is not None:
                character.equipped_armour[armour_type].id = itemIDNum
                self.items.append(character.equipped_armour[armour_type])
                self.armour.append(character.equipped_armour[armour_type])
                itemIDNum += 1
        for item in character.inventory:
            item.id = itemIDNum
            self.items.append(item)
            if item.is_Armour():
                self.armour.append(item)
            elif item.is_Weapon():
                self.weapons.append(item)
            itemIDNum += 1

        rand_index = rd.randint(0, len(self.spawn[character_type])-1)
        spawn_coords = self.spawn[character_type].pop(rand_index)

        character.coords = spawn_coords
        self.characterGrid[spawn_coords[0]][spawn_coords[1]] = character
        character.initialiseTurn()

        return character

    # Moves a character on the grid
    def moveCharacter(self, charID: int, newCoords: Tuple[int, int]):
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
    def moveObject(self, objID: int, newCoords: Tuple[int, int]):
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

    # Drops the characters weapon
    def dropWeapon(self, character: Character) -> None:  # Needs update to new weapon system
        raise NotImplementedError("Dropping weapons not implemented")

    # Drops the characters armour
    def dropArmour(self, character: Character) -> None:  # Needs update to new armour system
        raise NotImplementedError("Dropping armour not implemented")

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
    def is_validMovement(self, charID: int, newCoords: Tuple[int, int]):
        x, y = newCoords
        oldx, oldy = self.entities[charID].coords
        return self.entities[charID].movement >= calcPathDist((oldx, oldy), (x, y))

    # Checks if the character can move along the given path
    def is_validPath(self, charID: int, pathCoords: Tuple[int, int]):
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
    def is_validAttack(self, atkID: int, defID: int):
        atkx, atky = self.entities[atkID].coords
        defx, defy = self.entities[defID].coords

        radius = int(self.entities[atkID].reach/5)
        remaining_atks = self.entities[atkID].actions

        return abs(atkx - defx) <= radius and abs(atky - defy) <= radius and remaining_atks > 0
