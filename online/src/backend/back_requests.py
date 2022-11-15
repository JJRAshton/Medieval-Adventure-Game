from . import processing as pr


class Requests:

	def __init__(self):
		self.functions = pr.Track()

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
	def startRequest(self, map_number, player_quantity):

		self.functions.requestMapStart(map_number, player_quantity)

		return self.functions.returnPlayers(), self.functions.map_size

	# Requests the coords of characters with their IDs
	def locationsRequest(self):

		return self.functions.giveCharLoc()

	# Requests for info about a character
	def infoRequest(self, globalID):

		return self.functions.getInfo(globalID)
