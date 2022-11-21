class TurnNotificationSubscription():

    def __init__(self):
        #do nothing
        pass

    def notify(self, character_on_turn):
        # Do something
        pass

class TurnNotifier():

    def __init__(self):
        self.subscriptions = []
    
    def subscribe(self, subscription):
        # Pass in a subscription object (or an extension of TurnNotificationSubscription) with a 
        # notify(id) method, which will get called when a new turn passes.
        self.subscriptions.append(subscription)

    def announce(self, charecter_on_turn):
        # Call this to announce to all subscriptions that the turn has
        # changed
        for subscription in self.subcriptions:
            subscription.notify(charecter_on_turn)