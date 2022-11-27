import random as rd

from . import turn_manager as tn
from . import back as bk
from .turn_notifications import TurnNotifier
from ai.ai_manager import AIManager



# Converts an ID number to the index of its category's list
# 1: characters, 2: objects, 3: items
def id_to_local(globalID):
    if globalID < 100:
        category = 1
    elif globalID < 200:
        category = 2
    elif globalID < 300:
        category = 3
    else:
        category = None
    localID = globalID % 100

    return localID, category


# Function comments are in back_requests
class Hub:

    def __init__(self, turn_notification_subscription, ai_manager):
        self.map = 0
        self.map_size = (0, 0)

        self.chart = None
        self.turn_manager = None
        self.front_end_turn_notification_subscription = turn_notification_subscription
        self.ai_manager = ai_manager

    # Moves an entity to given coords
    def requestMove(self, globalID, coords):
        localID, category = id_to_local(globalID)
    
        if category == 2:
            self.chart.moveObject(localID, coords)
            return True

        elif category == 1:
            self.chart.moveCharacter(localID, coords)
            return True

        else:
            return False

    # Checks if a move is valid
    def requestMoveVerification(self, globalID, coords):
        localID, category = id_to_local(globalID)

        if category == 2 and self.chart.is_validCoords(coords):
            return True

        elif category == 1 and self.chart.is_validCoords(coords) and self.chart.is_validMovement(localID, coords):
            return True

        else:
            return False

    # Checks if an attack is valid and then attacks if so
    def requestAttack(self, globalID1, globalID2, attack_list=[0]):
        localID1, category1 = id_to_local(globalID1)
        localID2, category2 = id_to_local(globalID2)

        if self.chart.is_validAttack(localID1, localID2, category2):

            if category1 == 1:
                attacker = self.chart.characters[localID1]
            else:
                raise ValueError

            if category2 == 1:
                defender = self.chart.characters[localID2]
            elif category2 == 2:
                defender = self.chart.objects[localID2]
            else:
                raise ValueError
            
            indictor = attacker.attack(attack_list, defender)
            print(indictor)
            defender.checkAlive()
            if not defender.is_alive:
                if category2 == 1:
                    self.calcDrop(defender)
                else:
                    self.chart.dropInv(defender)

            return True
        else:
            return False

    # Generates the map
    def requestMapStart(self, n_players, mapNumber=1):
        self.map = mapNumber
        self.chart = bk.Back(self.map, n_players)

        turn_notifier = TurnNotifier()
        
        turn_notifier.subscribe(self.front_end_turn_notification_subscription)
        turn_notifier.subscribe(self.ai_manager)

        self.turn_manager = tn.TurnManager(self.chart, turn_notifier)
        self.map_size = self.chart.size

    # Starts the combat cycle, should only be called after requestMapStart
    def startCombat(self):
        self.turn_manager.start()

    # Returns the players names with their IDs
    def returnPlayers(self):
        players = []

        for player in self.chart.players:
            player_info = (player.id, player.name)
            players.append(player_info)
        
        return players

    # Ends turn and start the next one
    def endTurn(self):
        self.turn_manager.endTurn()

    # Gives the locations of all characters
    def giveCharLoc(self):
        char_locs = {}

        for character in self.chart.characters:
            char_locs[character.id] = character.coords

        return char_locs

        # Gives the locations of all characters
    def giveObjLoc(self):
        obj_locs = []

        for i_object in self.chart.objects:
            obj_info = (i_object.id, i_object.coords)
            obj_locs.append(obj_info)

        return obj_locs

    # Gives the locations of all characters
    def giveMapItemLoc(self):
        item_locs = []

        for item in self.chart.items:
            if not item.is_carried:
                item_info = (item.id, item.coords)
                item_locs.append(item_info)

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
            'Max_range': character.reach,
            'Health': character.health,
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

