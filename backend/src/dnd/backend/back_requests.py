from typing import Set, Tuple

from ..api.users import User
from .processing.turn_notifications import TurnNotificationSubscription
from . import processing as pr


class Requests:

    def __init__(self, turn_notification_subscription: TurnNotificationSubscription, ai_manager: TurnNotificationSubscription):
        ai_manager.bind_to(self)
        turn_notification_subscription.requests = self
        self.functions = pr.Hub(turn_notification_subscription, ai_manager)

    # Requests the generation of the given map
    def init(self, players: Set[User], map_number: int=1, builtin: bool=True):
        self.functions.requestMapStart(players, map_number, builtin)

        return self.functions.getPlayers(), self.functions.map_size

    # Requests to move an entity with ID 'globalID' to a given coords.
    # Returns true if the request is carried out and false if not.
    def moveRequest(self, globalID: int, coords: Tuple[int, int]):
        return self.functions.requestMove(globalID, coords)

    # Requests to verify whether a move is valid
    def moveVerificationRequest(self, globalID: int, coords: Tuple[int, int]):
        return self.functions.requestMoveVerification(globalID, coords)

    # Requests an attack to be carried out between entities by 'globalID1' upon 'globalID2'
    # Returns true if the request is carried out and false if not.
    def attackRequest(self, globalID1: int, globalID2: int) -> bool:
        return self.functions.requestAttack(globalID1, globalID2)

    # Starts the combat cycle
    def startRequest(self):
        self.functions.startCombat()

    # Requests the coords of characters with their IDs
    def locationsRequest(self):
        return self.functions.getCharLoc()

    # Request to end turn, no validation the request came from the right person
    def endTurnRequest(self):
        self.functions.endTurn()

    # Requests for info about a character
    def infoRequest(self, globalID: int):
        return self.functions.getInfo(globalID)
