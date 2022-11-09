# A set of all the currently connected users, may not be in a game
currentUsers = set()

class User:
    def __init__(self, socket, uuid):
        self.uuid = uuid
        self.socket = socket
        self.ready = False
        self.session = None
        currentUsers.add(self)

    def __str__(self):
        return f"User with id: {self.uuid}"

    def sessionRequest(self, jsonEvent):
        if self.session == None:
            raise ConnectionError
        self.sessionRequest(jsonEvent, user)