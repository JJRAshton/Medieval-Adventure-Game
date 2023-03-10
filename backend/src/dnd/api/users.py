# A set of all the currently connected users, may not be in a game
from typing import Set
from websockets.legacy.server import WebSocketServerProtocol as WebSocket


class User:
    def __init__(self, socket: WebSocket, uuid: int):
        self.uuid: int = uuid
        self.socket: WebSocket = socket
        self.ready: bool = False
        self.session = None
        currentUsers.add(self)

    def __str__(self):
        return f"User with id: {self.uuid}"

    def sessionRequest(self, jsonEvent: str):
        if self.session == None:
            raise ConnectionError
        self.session.sessionRequest(jsonEvent, self)

currentUsers: Set[User] = set()
