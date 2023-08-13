import unittest
import sys

from dnd.backend.processing.hub import Hub


class TestHub(unittest.TestCase):

    def runTest(self):
        """ Test movement on hub """
        class TurnSubscription():
            """ Utility subscription for tests """
            def notify(self, character_on_turn, is_player):
                """ We don't need to do anything here """
                pass
        sys.path.append('../')
        import dnd

        turn_subscription = TurnSubscription()
        hub = Hub(turn_subscription, turn_subscription)
        hub.requestMapStart(1, 1, True)
        hub.requestMove('character_1', (1,1))
        assert len(hub.getPlayers()) == 1, hub.getPlayers()
        assert len(hub.chart.characters) == 3, hub.chart.characters

if __name__ == '__main__':
    unittest.main()