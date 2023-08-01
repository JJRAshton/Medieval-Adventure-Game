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
        elif is_character(entID):
            self.chart.moveCharacter(entID, coords)
        else:
            raise ValueError
        return True

    # Checks if a move is valid
    def requestMoveVerification(self, entID, coords):
        if self.chart.is_validCoords(coords):
            return is_object(entID) or is_character(entID) and self.chart.is_validMovement(entID, coords)
        return False

    # Checks if an attack is valid and then attacks if so
    def requestAttack(self, entID1, entID2, attack_list=[0]):
        if not self.chart.is_validAttack(entID1, entID2):
            return False

        if entID1 < 100:
            attacker = self.chart.entities[entID1]
        else:
            raise ValueError

        defender = self.chart.entities[entID2]
        
        indicator = attacker.attack(attack_list, defender)
        print(indicator)
        defender.check_alive()
        if not defender.is_alive:
            if is_character(entID2):
                if defender.behaviour_type >= 2:
                    self.calcDrop(defender)
            else:
                self.chart.dropInv(defender)

        return True

    # Generates the map
    def requestMapStart(self, n_players, map, using_builtin_map):
        self.chart = bk.Back(map, n_players, using_builtin_map)

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
        return [(player.id, player.name) for player in self.chart.players]

    # Ends turn and start the next one
    def endTurn(self):
        self.turn_manager.endTurn()

    # Returns the locations of all characters
    def getCharLoc(self):
        return {character.id: character.coords for character in self.chart.characters}

    # Returns the locations of all objects
    def getObjLoc(self):
        return {obj.id: obj.coords for obj in self.chart.objects}

    # Returns the locations of all items on map
    def getMapItemLoc(self):
        return {item.id: item.coords for item in self.chart.items if not item.is_carried}

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
            'Max_health': character.max_health,
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
                    'Name': character.equipped_armour[location].name if character.equipped_armour[location] is not None else 'N/A'
                }
                for location in character.equipped_armour},

            'Weapons': {
                location: {
                    'Name': character.equipped_weapons[location].name,
                    'Characteristic':
                        'Light' if character.equipped_weapons[location].has_trait('Light') else
                        'Loading' if character.equipped_weapons[location].has_trait('Loading') else
                        'Normal'
                }
                for location in character.equipped_weapons if character.equipped_weapons[location] is not None},

            'Inventory': [item.name for item in character.inventory],
        }

        return infoDict

