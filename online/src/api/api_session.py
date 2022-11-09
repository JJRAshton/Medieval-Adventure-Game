import websockets
import json

class APISession:
    """The main API, this should probably create a dnd game interacting with the backend?
    Joe needs to decide how he wants this to be done """
    def __init__(self, playerPool):
        self.playerPool = playerPool # This is a set of api.users.User
        for player in playerPool:
            player.session = self
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
