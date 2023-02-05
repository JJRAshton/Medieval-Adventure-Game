from .brain import Brain1


class AIManager:
    # Gets prompted to make a move or decision by a backend endpoint,
    # then makes a call to the backend API.

    def __init__(self):
        # This is the access point to the backend
        self.brains = []
        self.backend = None

    def bind_to(self, backend):
        self.backend = backend

    def notify(self, turn_character_id, is_player):
        if not self.backend:
            raise ValueError("AI manager has not been to a request API")
        if not is_player:
            self.takeTurn(self.backend, turn_character_id)

# Sorry for putting backend everywhere, don't know what to do with it
    def takeTurn(self, backend, id):
        # Make a brain
        ai_brain = Brain1(backend, id)
        # Choose target for approaching/attacking
        target = ai_brain.choose_target()
        print(target)
        # Run up to target and keep attacking if in range
        ai_brain.approach_and_attack_target(backend, target)
        # Turn has ended
        backend.endTurnRequest()
        print('AI turn has ended')

    def checkReaction(self):
        # I think we've agreed not to do reactions for now, but this is where it would go
        raise NotImplementedError

