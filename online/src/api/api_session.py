import json
import websockets
from backend import Requests
from .api_turn_notification_subscription import APITurnNotificationSubscription


class APISession:
    """The main API, this should probably create a dnd game interacting with the backend?
    Joe needs to decide how he wants this to be done """
    def __init__(self, playerPool):
        self.playerPool = playerPool # This is a set of api.users.User
        for player in playerPool:
            player.session = self
        
        turnNotifier = APITurnNotificationSubscription(playerPool)

        self.backend = Requests(turnNotifier)
        self.translator = PythonToJSONTranslator()

        # Starting the DnD encounter:
        character_info_list, size = self.backend.init(len(playerPool), 1)
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
        print(len(self.playerPool))
        websockets.broadcast({user.socket for user in self.playerPool}, json.dumps(message))

    def sendToUserWithID(self, message, uuid):
        for user in self.playerPool:
            if user.uuid == uuid:
                user.socket.send(message)
                # Once we've found the user, we're done as the id are unique
                return
            
    def sessionRequest(self, jsonEvent, user):
        # This will probably be the main function, it is
        # called directly by the user which is maybe a weird code flow?
        print(jsonEvent)

        if jsonEvent["event"] == "moveRequest":
            print(jsonEvent["route"])
            try:
                playerID = int(jsonEvent["playerID"])
            except:
                print(f"Could not convert player ID to int {jsonEvent['playerID']}")
                return
            # move = self.backend.moveRequest(jsonEvent["playerID"], jsonEvent["coords"])
            if len(jsonEvent["route"]) < 2:
                return
            for coord in jsonEvent["route"][1:]:
                print(f"coord {coord}")
                if self.backend.moveVerificationRequest(playerID, coord):
                    print("Move verified")
                    if not self.backend.moveRequest(playerID, coord):
                        # If the move goes through, update the player
                        break
                    print("Move succeeded") 
                else:
                    break
                                    
            locations = self.backend.locationsRequest()
            characterLocations = [(characterID, locations[characterID]) for characterID in locations]
            print(f"Broadcasting locations: {characterLocations}")
            self.broadcast({"responseType": "mapUpdate", "characters": characterLocations})
            
        elif jsonEvent["event"] == "attackRequest":
            attack=self.backend.attackRequest(jsonEvent["playerID"], jsonEvent["enemyID"])
            output = json.dumps({
                "responseType": "attackResult",
                "attackResult": str(attack)
            })
            user.socket.send(output)

        elif jsonEvent["event"] == "mapRequest":
            map = self.backend.locationsRequest()
            output = self.translator.map_to_json(map)
            user.socket.send(output)

        elif jsonEvent["event"] == "endTurnRequest":
            self.backend.endTurnRequest()



class PythonToJSONTranslator:

    def translate(self, jsonDictionary):
        return json.dumps(jsonDictionary)
 
    def map_to_json(self, loc):
        dictionary={}
        for info in loc:
            id_number=info[0]
            coords=info[1]
            x,y = coords
            dictionary[f'ID{id_number}']=[str(x), str(y)]
        return dictionary
