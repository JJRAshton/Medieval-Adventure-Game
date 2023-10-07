import json
from typing import Set
import websockets

from .. import settings

from ..ai.ai_manager import AIManager
from ..api.api_turn_notification_subscription import APITurnNotificationSubscription
from ..backend.back_requests import Requests
from .users import User


class APISession:
    """The main API, this should probably create a dnd game interacting with the backend?
    Joe needs to decide how he wants this to be done """
    def __init__(self, playerPool: Set[User]):
        if settings.LOG_LEVEL == settings.LogLevel.OFF:
            print("New game starting...")
        self.playerPool = playerPool
        for player in playerPool:
            player.session = self

        turnNotifier = APITurnNotificationSubscription(playerPool)

        self.backend = Requests(turnNotifier, AIManager())
        self.translator = PythonToJSONTranslator()

        # Starting the DnD encounter:
        character_info_list, size = self.backend.init(len(playerPool))
        mapWidth, mapHeight = size
        if len(character_info_list) != len(playerPool):
            raise ValueError("Wrong number of players created on games start")
        locations = self.backend.locationsRequest()
        characterLocations = [(characterID, locations[characterID]) for characterID in locations]
        for character_info, user in zip(character_info_list, playerPool):
            websockets.broadcast(
                {user.socket},
                self.translator.translate({
                    "responseType": "gameStart",
                    "mapStatus": {"mapWidth": mapWidth, "mapHeight": mapHeight},
                    "playerID": character_info[0],
                    "characters": characterLocations
                }))
        self.backend.startRequest()

    # Called by the backend, sends a json message
    def broadcast(self, message):
        if settings.LOG_LEVEL == settings.LogLevel.ON:
            print(f"Broadcasting locations: {message}")

        websockets.broadcast({user.socket for user in self.playerPool}, json.dumps(message)) # type: ignore

    def sendToUserWithID(self, message, uuid: int):
        for user in self.playerPool:
            if user.uuid == uuid:
                user.socket.send(message)
                return
            
    def sessionRequest(self, jsonEvent: str, user: User):
        if settings.LOG_LEVEL == settings.LogLevel.ON:
            print(f"Receiving request: {jsonEvent}")

        if not "event" in jsonEvent:
            raise ValueError(f"Request {jsonEvent} does not declare its type")
        if jsonEvent["event"] == "moveRequest":
            try:
                playerID = jsonEvent["playerID"]
            except Exception:
                raise ValueError("Could not convert player ID")
            if len(jsonEvent["route"]) < 2:
                return
            for coord in jsonEvent["route"][1:]:
                if self.backend.moveVerificationRequest(playerID, coord):
                    if not self.backend.moveRequest(playerID, coord):
                        break
                else:
                    break

            locations = self.backend.locationsRequest()
            characterLocations = [(characterID, locations[characterID]) for characterID in locations]
            self.broadcast({"responseType": "mapUpdate", "characters": characterLocations})

        elif jsonEvent["event"] == "playerInfoRequest":
            characterID = jsonEvent["characterID"]
            
            output = json.dumps({
                "responseType": "playerInfo",
                "characterID": characterID,
                "playerInfo": self.backend.infoRequest(characterID)
            })
            websockets.broadcast({user.socket}, output) # type: ignore

        elif jsonEvent["event"] == "attackRequest":
            attack = self.backend.attackRequest(jsonEvent["playerID"], jsonEvent["enemyID"])
            output = json.dumps({
                "responseType": "attackResult",
                "attackResult": str(attack)
            })
            websockets.broadcast({user.socket}, output) # type: ignore

        elif jsonEvent["event"] == "mapRequest":
            dnd_map = self.backend.locationsRequest()
            output = self.translator.map_to_json(dnd_map)
            websockets.broadcast({user.socket}, output) # type: ignore

        elif jsonEvent["event"] == "endTurnRequest":
            self.backend.endTurnRequest()

        else:
            raise ValueError(f"Event type: '{jsonEvent['event']}' was not recognised")



class PythonToJSONTranslator:

    def translate(self, jsonDictionary):
        return json.dumps(jsonDictionary)
 
    def map_to_json(self, loc):
        dictionary = {}
        for info in loc:
            id_number = info[0]
            coords = info[1]
            x, y = coords
            dictionary[f'ID{id_number}'] = [str(x), str(y)]
        return dictionary
