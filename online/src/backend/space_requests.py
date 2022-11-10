from space import Chart
from conversion_functions import Convert

class Requester:

	def __init__(self, mapNumber):
		self.chart = Chart(mapNumber)
		self.functions = Convert()
		

	def moveRequest(self, globalID, coords):

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


	def attackRequest(self, globalID1, globalID2):

		if is_validAttack(globalID1, globalID2):
			attacker = self.chart.entities[globalID1]
			defender = self.chart.entities[globalID2]
			
			attacker.attack(defender)
			request = True
		else:
			request = False

		return request