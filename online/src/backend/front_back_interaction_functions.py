from .back import Back
from .turns import Time
import random as rd


# Converts an ID number to the index of its category's list
# 1: characters, 2: objects, 3: items
def id_to_local(globalID):
	if globalID < 100:
		category = 1
	elif globalID < 200:
		category = 2
	elif globalID < 300:
		category = 3
	else:
		category = None
	localID = globalID % 100

	return localID, category


# Function comments are in back_requests
class Requester:

	def __init__(self):
		self.map = 0

		self.chart = None
		self.time = None

	# Moves an entity to given coords
	def requestMove(self, globalID, coords):
		localID, category = id_to_local(globalID)
		completed = False
	
		if category == 2:
			self.chart.moveObject(localID, coords)

		elif category == 1:
			self.chart.moveCharacter(localID, coords)
			completed = True
			if self.chart.checkOpportunity(localID, coords):
				pass  # makes opportunity attacks
	
		return completed

	# Checks if a move is valid
	def requestMoveVerification(self, globalID, coords):
		localID, category = id_to_local(globalID)
		valid = False

		if category == 2 and self.chart.is_validCoords(coords):
			valid = True
		elif category == 1 and self.chart.is_validCoords(coords) and self.chart.is_validMovement(localID, coords):
			valid = True

		return valid

	# Checks if an attack is valid and then attacks if so
	def requestAttack(self, globalID1, globalID2):
		localID1, category1 = id_to_local(globalID1)
		localID2, category2 = id_to_local(globalID2)

		if self.chart.is_validAttack(localID1, localID2, category2):
			if category1 == 1:
				attacker = self.chart.characters[localID1]
			else:
				raise ValueError
			if category2 == 1:
				defender = self.chart.characters[localID2]
			elif category2 == 2:
				defender = self.chart.objects[localID2]
			else:
				raise ValueError
			
			attacker.attack(defender)
			defender.checkHealth()
			if not defender.is_alive:
				if category2 == 1:
					self.calcDrop(defender)
				else:
					self.chart.dropInv(defender)

			return True
		else:
			return False

	# Generates the map
	def requestMapStart(self, mapNumber, n_players):
		self.map = mapNumber
		self.chart = Back(self.map, n_players)
		self.time = Time(self.chart)

	# Starts the turns
	def requestTimeStart(self):
		self.time.start(self.chart)

	# Returns the players names with their IDs
	def returnPlayers(self):
		players = []

		for player in self.chart.players:
			player_info = (player.id, player.name)
			players.append(player_info)
		
		return players

	# Gives the locations of all characters
	def giveCharLoc(self):
		char_locs = []

		for character in self.chart.characters:
			char_info = (character.id, character.coords)
			char_locs.append(char_info)

		return char_locs

		# Gives the locations of all characters
	def giveObjLoc(self):
		obj_locs = []

		for i_object in self.chart.objects:
			obj_info = (i_object.id, i_object.coords)
			obj_locs.append(obj_info)

		return obj_locs

	# Gives the locations of all characters
	def giveMapItemLoc(self):
		item_locs = []

		for item in self.chart.items:
			if not item.is_carried:
				item_info = (item.id, item.coords)
				item_locs.append(item_info)

		return item_locs

	# Calculates whether a character will drop an item (upon death)
	def calcDrop(self, character):
		prob = character.difficulty + 10
		roll = rd.randint(1, prob)

		if roll <= 5:
			if roll == 1:
				self.chart.dropWeapon(character)
			elif roll == 2:
				self.chart.dropArmour(character)
			else:
				self.chart.dropInv(character)
