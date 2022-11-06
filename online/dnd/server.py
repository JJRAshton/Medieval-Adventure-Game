

class Server(api.APIServer):
    
    def moveRequest(self, move):
        
        raise NotImplementedError

    def attackRequest(self, atk):
        raise NotImplementedError