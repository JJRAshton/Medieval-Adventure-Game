import pickle as pkl
import character as ch

class Map:
	# IDs for items around the map from generation
	mapItemIDs = {
	0: 'grass' # 0-99 surfaces
	100: 'orc' # 100-199 monsters
	# 200-299 terrain features
	}
	def __init__(self, mapNumber):
		self.map = mapNumber
		self.grid = []

		self.getMap()

	#Loads in the map from the map number given
	def getMap(self):
		self.grid = pkl.load(open('maps/map'+str(self.map)+'.pkl','rb'))

	#Gets what ID is in cell at given coords and places the relevant item
	def createCell(self, coords, entityID):
		item = self.grid[coords[0]][coords[1]]
		self.grid[coords[0][coords[1]] = ch.Monster(Map.mapItemIDs[item], entityID)

