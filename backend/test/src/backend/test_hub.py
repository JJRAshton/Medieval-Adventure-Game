from unittest import TestCase

from dnd.backend.processing.hub import Hub

import os 

resource_dir = os.path.split(os.path.realpath(__file__))[0].replace("/src/", "/resources/") + "/"

class TestHub(TestCase):

    def testMovement(self):
        i = 0
        class TurnSubscription():
            def notify(character_on_turn, is_player):
                print(character_on_turn, is_player)

        turn_subscription = TurnSubscription()
        hub = Hub(turn_subscription, turn_subscription)
        map_uri = resource_dir+"back_map"
        hub.requestMapStart(1, map_uri, False)
        assert len(hub.getPlayers()) == 1, hub.returnPlayers()
        assert len(hub.chart.characters) == 6, hub.chart.characters


