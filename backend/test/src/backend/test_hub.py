from unittest import TestCase

from dnd.backend.processing.hub import Hub

class TestHub(TestCase):

    def testMovement(self):
        hub = Hub(turn_notification_subscription, ai_manager)
        first_chr = back.characters[0]
        first_chr_coords = first_chr.coords


