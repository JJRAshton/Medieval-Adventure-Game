import json
import websockets
from backend.back_requests import Requests


class APISession:
    """The main API, this should probably create a dnd game interacting with the backend?
    Joe needs to decide how he wants this to be done """
    def __init__(self, playerPool):
        self.playerPool = playerPool # This is a set of api.users.User
        for player in playerPool:
            player.session = self
        self.backend = Requests()
        self.translator = PythonToJSONTranslator()

        # Starting the DnD encounter:
        character_info_list, size = self.backend.startRequest(len(playerPool), 1)
        mapWidth, mapHeight = size
        if len(character_info_list) != len(playerPool):
            raise ValueError("Wrong number of players created on games start")
        for character_info, user in zip(character_info_list, playerPool):
            websockets.broadcast(
                {user.socket},
                self.translator.translate({
                    "responseType": "gameStart",
                    "mapStatus": {"mapWidth": mapWidth, "mapHeight": mapHeight},
                    "playerID": character_info[0],
                    "players": "players"
                }))

    # Called by the backend, sends a json message
    def broadcast(self, message):
        websockets.broadcast({user.socket for user in self.playerPool}, message)

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
        if jsonEvent["event"] == "newPlayer":
            id, name = self.backend.createPlayerRequest()
            output = json.dumps({
            "responseType": "newPlayer",
            "newPlayerId": str(id)
            })
            user.socket.send(output)

        if jsonEvent["event"] == "moveRequest":
            move = self.backend.moveRequest(jsonEvent["playerID"], jsonEvent["coords"])
            output = json.dumps({
            "responseType": "moveResult",
            "moveResult": str(move)
            })
            user.socket.send(output)
            
        if jsonEvent["event"] == "attackRequest":
            attack=self.backend.attackRequest(jsonEvent["playerID"], jsonEvent["enemyID"])
            output = json.dumps({
            "responseType": "attackResult",
            "attackResult": str(attack)
            })
            user.socket.send(output)

        if jsonEvent["event"] == "mapRequest":
            map=self.backend.locationsRequest()
            output = self.translator.map_to_json(map)
            user.socket.send(output)



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

