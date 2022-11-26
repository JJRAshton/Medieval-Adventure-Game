import websockets
import json

from backend import TurnNotificationSubscription

class APITurnNotificationSubscription(TurnNotificationSubscription):

    def __init__(self):
        super().__init__(self)

    def notify(self, character_on_turn, is_player):
        websockets.broadcast({user.socket for user in self.playerPool}, json.dumps(message))


