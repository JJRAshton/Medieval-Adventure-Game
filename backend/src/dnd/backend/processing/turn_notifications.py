from typing import List


class TurnNotificationSubscription:
    # This should be inherited, and the notify method overridden

    def __init__(self):
        #do nothing
        pass

    def notify(self, turn_character_id: int, is_player: bool):
        # Do something
        pass


class TurnNotifier:

    def __init__(self) -> None:
        self.subscriptions: List[TurnNotificationSubscription] = []
    
    def subscribe(self, subscription: TurnNotificationSubscription) -> None:
        # Pass in a subscription object (or an extension of TurnNotificationSubscription) with a 
        # notify(id) method, which will get called when a new turn passes.
        self.subscriptions.append(subscription)

    def announce(self, character_on_turn: int, is_player: bool) -> None:
        # Call this to announce to all subscriptions that the turn has
        # changed
        for subscription in self.subscriptions:
            subscription.notify(character_on_turn, is_player)