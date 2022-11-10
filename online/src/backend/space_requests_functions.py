from space import Chart

#Converts an ID number to the index of its category's list
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
		
	def requestMove(self, globalID, coords):
		localID, category = self.functions.id_to_local(globalID)
	
		if category == 2 and self.chart.is_validCoords(coords):
			self.chart.moveObject(localID, coords)
		elif category == 1 and self.chart.is_validCoords(coords) and self.chart.is_validMovement(localID, coords):
			if self.chart.checkOpportunity(localID, coords):
				pass # makes opportunity attacks
			self.chart.moveCharacter(localID, coords)
			completed = True
		else:
			completed = False
	
		return completed

	def requestAttack(self, globalID1, globalID2):

		if is_validAttack(globalID1, globalID2):
			attacker = self.chart.entities[globalID1]
			defender = self.chart.entities[globalID2]
			
			attacker.attack(defender)
			completed = True
		else:
			completed = False

		return request
	
	def requestStart(self, mapNumber):
		self.map = mapNumber
		self.chart = Chart(self.map)
		