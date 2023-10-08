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

        self.player_name = None
        self.player_class = None
        self.player_weapon = None

    def __str__(self):
        return f"User with id: {self.uuid}"

    def sessionRequest(self, jsonEvent: str):
        if self.session == None:
            raise ConnectionError
        self.session.sessionRequest(jsonEvent, self)

    def set_character_preferences(self, player_name, player_class, player_weapon):
        self.player_name = player_name if player_name else None
        self.player_class = player_class if player_class else None
        self.player_weapon = player_weapon if player_weapon else None

    def clear_character_preferences(self):
        self.player_name = None
        self.player_class = None
        self.player_weapon = None

currentUsers: Set[User] = set()
