import json
import websockets
from backend.back_requests import BackRequests

class APISession:
    """The main API, this should probably create a dnd game interacting with the backend?
    Joe needs to decide how he wants this to be done """
    def __init__(self, playerPool):
        self.playerPool = playerPool # This is a set of api.users.User
        for player in playerPool:
            player.session = self
        self.backend = BackRequests()
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

class JSONToPythonTranslator:
    def __init__(self):
        raise NotImplementedError

    def translate(json):
        raise NotImplementedError

class PythonToJSONTranslator:
    def __init__(self):
        raise NotImplementedError

    def __init__(self, jsonDictionary):
        return json.dumps(jsonDictionary)
