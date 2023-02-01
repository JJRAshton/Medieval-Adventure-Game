from . import processing as pr
from dnd.ai.ai_manager import AIManager


class Requests:

    def __init__(self, turn_notification_subscription):
        ai_manager = AIManager(self)
        turn_notification_subscription.requests = self
        self.functions = pr.Hub(turn_notification_subscription, ai_manager)

    # Requests to move an entity with ID 'globalID' to a given coords.
    # Returns true if the request is carried out and false if not.
    def moveRequest(self, globalID, coords):

        completed = self.functions.requestMove(globalID, coords)
        
        return completed

    # Requests to verify whether a move is valid
    def moveVerificationRequest(self, globalID, coords):
        valid = self.functions.requestMoveVerification(globalID, coords)

        return valid

    # Requests an attack to be carried out between entities by 'globalID1' upon 'globalID2'
    # Returns true if the request is carried out and false if not.
    def attackRequest(self, globalID1, globalID2):

        completed = self.functions.requestAttack(globalID1, globalID2)

        return completed
    

    # Requests the generation of the given map
    def init(self, player_quantity, map_number=1):

        self.functions.requestMapStart(player_quantity, map_number)

        return self.functions.returnPlayers(), self.functions.map_size

    # Starts the combat cycle
    def startRequest(self):

        self.functions.startCombat()

    # Requests the coords of characters with their IDs
    def locationsRequest(self):

        return self.functions.giveCharLoc()

    # Request to end turn, no validation the request came from the right person
    def endTurnRequest(self):
        self.functions.endTurn()

    # Requests for info about a character
    def infoRequest(self, globalID):

        return self.functions.getInfo(globalID)
