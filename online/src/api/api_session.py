import json
import websockets
from src import backend as bk


class APISession:
    """The main API, this should probably create a dnd game interacting with the backend?
    Joe needs to decide how he wants this to be done """
    def __init__(self, playerPool):
        self.playerPool = playerPool # This is a set of api.users.User
        for player in playerPool:
            player.session = self
        self.backend = BackRequests()
        self.translator = PythonToJSONTranslator()
        # This should create a DnD session in the backend, 

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
    def __init__(self):
        raise NotImplementedError

    def __init__(self, jsonDictionary):
        return json.dumps(jsonDictionary)
 
    def map_to_json(self, loc):
        dictionary={}
        for info in loc:
            id_number=info[0]
            coords=info[1]
            x,y = coords
            dictionary[f'ID{id_number}']=[str(x), str(y)]

