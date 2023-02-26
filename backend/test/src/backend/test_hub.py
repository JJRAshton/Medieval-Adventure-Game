from unittest import TestCase

from dnd.backend.processing.hub import Hub

import os 

resource_dir = os.path.split(os.path.realpath(__file__))[0].replace("/src/", "/resources/") + "/"

class TestHub(TestCase):

    def test_movement(self):
        """ Test movement on hub """
        class TurnSubscription():
            """ Utility subscription for tests """
            def notify(self, character_on_turn, is_player):
                """ We don't need to do anything here """
                pass

        turn_subscription = TurnSubscription()
        hub = Hub(turn_subscription, turn_subscription)
        map_uri = resource_dir+"back_map"
        hub.requestMapStart(1, map_uri, False)
        hub.requestMove
        assert len(hub.getPlayers()) == 1, hub.getPlayers()
        assert len(hub.chart.characters) == 6, hub.chart.characters


