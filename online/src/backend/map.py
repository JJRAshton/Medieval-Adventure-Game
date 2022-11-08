import pickle as pkl

class Map:
	def __init__(self, mapNumber):
		self.map = mapNumber
		self.grid = []

		self.getMap()

	#Loads in the map from the map number given
	def getMap(self):
		self.grid = pkl.load(open('maps/map'+str(self.map)+'.pkl','rb'))

	#Gets what is in cell at given coords
	def getCell(self, coords):
