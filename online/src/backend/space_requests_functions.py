from space import Chart


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


class Requester:

	def __init__(self):
		self.map = 0
		self.chart = None

	def requestMove(self, globalID, coords):
		localID, category = id_to_local(globalID)
		completed = False
	
		if category == 2 and self.chart.is_validCoords(coords):
			self.chart.moveObject(localID, coords)
		elif category == 1 and self.chart.is_validCoords(coords) and self.chart.is_validMovement(localID, coords):
			if self.chart.checkOpportunity(localID, coords):
				pass  # makes opportunity attacks
			self.chart.moveCharacter(localID, coords)
			completed = True
	
		return completed

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
			completed = True
		else:
			completed = False

		return completed
	
	def requestStart(self, mapNumber):
		self.map = mapNumber
		self.chart = Chart(self.map)
		
	def requestPlayerCreation(self):
		
		player = self.chart.createPlayer()
		playerID = player.id
		playerName = player.name
		
		return playerID, playerName
