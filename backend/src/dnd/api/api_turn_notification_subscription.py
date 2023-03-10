import websockets
import json

from ..backend import TurnNotificationSubscription
from .users import User

class APITurnNotificationSubscription(TurnNotificationSubscription):

    def __init__(self, playerPool: Set[User]):
        super().__init__()
        self.socketPool = {user.socket for user in playerPool}
        self.requests = None

    def notify(self, character_on_turn, is_player):
        websockets.broadcast(self.socketPool, json.dumps( # type: ignore
            {
                "responseType": "turnNotification",
                "onTurnID": character_on_turn,
                "charactersUpdate": self.getCharactersUpdate()
            }
        ))
    
    def getCharactersUpdate(self):
        if self.requests is None:
            raise ValueError("Requests not initialised")
        locations = self.requests.locationsRequest()
        return {charcter_id: self.getUpdateForCharacter(charcter_id, locations[charcter_id]) for charcter_id in locations}

    def getUpdateForCharacter(self, id, location):
        characterInfo = self.requests.infoRequest(id)
        return {
            "Health": characterInfo["Health"],
            "coords": location
        }




