import random as rd
from typing import Tuple

from . import turn_manager as tn
from . import back as bk
from .turn_notifications import TurnNotificationSubscription, TurnNotifier


# Checks for what type of entity the id is
def is_character(entID: int) -> bool:
    return 0 <= entID < 100


def is_object(entID: int) -> bool:
    return 100 <= entID < 200


def is_item(entID: int) -> bool:
    return 200 <= entID < 300


# Function comments are in back_requests
class Hub:

    def __init__(self, turn_notification_subscription: TurnNotificationSubscription, ai_manager: TurnNotificationSubscription):
        self.map_size = (0, 0)

        self.chart = None
        self.turn_manager = None
        self.front_end_turn_notification_subscription = turn_notification_subscription
        self.ai_manager = ai_manager

    # Moves an entity to given coords
    def requestMove(self, entID: int, coords: Tuple[int, int]):
    
        if is_object(entID):
            self.chart.moveObject(entID, coords)
            return True

        elif is_character(entID):
            self.chart.moveCharacter(entID, coords)
            return True

        else:
            raise ValueError

    # Checks if a move is valid
    def requestMoveVerification(self, entID, coords):

        if is_character(entID) and self.chart.is_validCoords(coords) and self.chart.is_validMovement(entID, coords):
            return True

        elif is_object(entID) and self.chart.is_validCoords(coords):
            return True

        else:
            return False

    # Checks if an attack is valid and then attacks if so
    def requestAttack(self, entID1, entID2, attack_list=[0]):

        if self.chart.is_validAttack(entID1, entID2):

            if entID1 < 100:
                attacker = self.chart.entities[entID1]
            else:
                raise ValueError

            defender = self.chart.entities[entID2]
            
            indicator = attacker.attack(attack_list, defender)
            print(indicator)
            defender.checkAlive()
            if not defender.is_alive:
                if is_character(entID2):
                    if defender.behaviour_type >= 2:
                        self.calcDrop(defender)
                else:
                    self.chart.dropInv(defender)

            return True
        else:
            return False

    # Generates the map
    def requestMapStart(self, n_players, map, builtin):
        self.chart = bk.Back(map, n_players, builtin)

        turn_notifier = TurnNotifier()
        
        turn_notifier.subscribe(self.front_end_turn_notification_subscription)
        turn_notifier.subscribe(self.ai_manager)

        self.turn_manager = tn.TurnManager(self.chart, turn_notifier)
        self.map_size = self.chart.size

    # Starts the combat cycle, should only be called after requestMapStart
    def startCombat(self):
        self.turn_manager.start()

    # Returns the players names with their IDs
    def getPlayers(self):
        players = []

        for player in self.chart.players:
            player_info = (player.id, player.name)
            players.append(player_info)
        
        return players

    # Ends turn and start the next one
    def endTurn(self):
        self.turn_manager.endTurn()

    # Returns the locations of all characters
    def getCharLoc(self):
        char_locs = {}

        for character in self.chart.characters:
            char_locs[character.id] = character.coords

        return char_locs

    # Returns the locations of all objects
    def getObjLoc(self):
        obj_locs = {}

        for i_object in self.chart.objects:
            obj_locs[i_object.id] = i_object.coords

        return obj_locs

    # Returns the locations of all items on map
    def getMapItemLoc(self):
        item_locs = {}

        for item in self.chart.items:
            if not item.is_carried:
                item_locs[item.id] = item.coords

        return item_locs

    # Calculates whether a character will drop an item (upon death)
    def calcDrop(self, character):
        prob = character.difficulty + 10
        roll = rd.randint(1, prob)

        if roll <= 5:
            if roll == 1:
                self.chart.dropWeapon(character)
            elif roll == 2:
                self.chart.dropArmour(character)
            else:
                self.chart.dropInv(character)

    # Gets information about a character
    def getInfo(self, charID):
        if charID >= 100:
            raise ValueError

        character = self.chart.characters[charID]
        infoDict = {
            'Team': character.team,
            'Remaining_movement': character.movement,
            'Range': character.range,
            'Reach': character.reach,
            'Health': character.health,
            'Max_health': character.maxHealth,
            'Action_number': character.actions,

            'Stats': {
                stat: character.stat[stat]
                for stat in character.stat},

            'Attacks': [{
                'Name': attack.name,
                'Weapon': attack.from_weapon.name,
                'Range': attack.from_weapon.range
            } for attack in character.attack_options],

            'Armour': {
                location: {
                    'Name': character.equippedArmour[location].name if character.equippedArmour[location] is not None else 'N/A'
                }
                for location in character.equippedArmour},

            'Weapons': {
                location: {
                    'Name': character.equippedWeapons[location].name,
                    'Characteristic':
                        'Light' if character.equippedWeapons[location].is_light else
                        'Loading' if character.equippedWeapons[location].is_loading else
                        'Normal'
                }
                for location in character.equippedWeapons if character.equippedWeapons[location] is not None},

            'Inventory': [item.name for item in character.inventory],
        }

        return infoDict

