from space import Chart
from space_requests_functions import Requester

class MollyRequests:

	def __init__(self):
		self.functions = Requester()
		
		
	# Requests to move an entity with ID 'globalID' to a given coords.
	# Returns true if the request is carried out and false if not.
	def moveRequest(self, globalID, coords):

		completed = self.functions.requestMove(globalID, coords)
		
		return completed


	# Requests an attack to be carried out between entities by 'globalID1' upon 'globalID2'
	# Returns true if the request is carried out and false if not.
	def attackRequest(self, globalID1, globalID2):

		completed = self.functions.requestAttack(globalID1, globalID2)

		return completed
	
	# Requests the generation of the given map
	def startRequest(self, mapNumber):
        
		self.functions.requestStart(mapNumber)
    