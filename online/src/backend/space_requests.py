from space import Chart

class Requester:

	def __init__(self, mapNumber):
		self.chart = Chart(mapNumber)
		

	def moveRequest(self, id, coords):

		if self.chart.validateMove(id, coords):
			self.chart.moveEntity(id, coords)
			request = True
		else:
			request = False

		return request


	def attackRequest(self, id1, id2):

		if validateAttack(id1, id2):
			attacker = self.chart.entities[id1]
			defender = self.chart.entities[id2]
			
			attacker.attack(defender)
			request = True
		else:
			request = False

		return request