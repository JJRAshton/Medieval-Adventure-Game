from backend.front_back_interaction_functions import Requester


class BackRequests:

	def __init__(self):
		self.functions = Requester()

	# Requests to move an entity with ID 'globalID' to a given coords.
	# Returns true if the request is carried out and false if not.
	def moveRequest(self, globalID, coords):

		completed = self.functions.requestMove(globalID, coords)
		
		return completed

	# Requests to verify whether a move is valid
	def moveVerificationRequest(self, globalID, coords):

		valid = self.functions.requestMoveVerification(globalID, coords)

		return valid

	# Requests an attack to be carried out between entities by 'globalID1' upon 'globalID2'
	# Returns true if the request is carried out and false if not.
	def attackRequest(self, globalID1, globalID2):

		completed = self.functions.requestAttack(globalID1, globalID2)

		return completed
	
	# Requests the generation of the given map
	def startRequest(self, mapNumber, playerNumber):

		self.functions.requestMapStart(mapNumber, playerNumber)

		return self.functions.returnPlayers()

	# Requests the coords of characters with their IDs
	def locationRequest(self):

		return self.functions.giveCharLoc()

	# Requesting the creation of a new player has been removed - they are returned upon the creation of the map
