from .brain import Brain
class AIManager:
    # Gets prompted to make a move or decision by a backend endpoint,
    # then makes a call to the backend API.

    def __init__(self, backend):
        # This is the access point to the backend
        self.brains = []

    def takeTurn(self, id):
        # Called by the backend
        raise NotImplementedError
    
    def checkReaction(self):
        # I think we've agreed not to do reactions for now, but this is where it would go
        raise NotImplementedError

