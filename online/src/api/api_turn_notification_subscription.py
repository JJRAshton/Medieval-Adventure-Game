import websockets
import json

from backend import TurnNotificationSubscription

class APITurnNotificationSubscription(TurnNotificationSubscription):

    def __init__(self, playerPool):
        super().__init__()
        self.socketPool = {user.socket for user in playerPool}

    def notify(self, character_on_turn, is_player):
        websockets.broadcast(self.socketPool, json.dumps(
            {
                "responsType": "turnNotification",
                "onTurnID": character_on_turn
            }
        ))


