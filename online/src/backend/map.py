import pickle as pkl
import character as ch

class Map:
	# IDs for items around the map from generation
	mapItemIDs = {
	1: 'orc' # 1-100 monsters
	# 101-200 NPCs
	# 201-300 terrain features
	}
	def __init__(self, mapNumber):
		self.map = mapNumber
		self.entities = []

		self.getMap()

	#Loads in the map from the map number given
	def getMap(self):
		self.entities = pkl.load(open('maps/map'+str(self.map)+'.pkl','rb'))

	#Gets what ID is in cell at given coords and places the relevant item
	def createCell(self, coords, entityID):
		itemID = self.grid[coords[0]][coords[1]]
		if itemID > 200:
			self.grid[coords[0][coords[1]] = ch.Object(Map.mapItemIDs[itemID], entityID)
			self.grid[coords[0][coords[1]].coords = coords
		elif itemID > 100:
			self.grid[coords[0][coords[1]] = ch.NPC(Map.mapItemIDs[itemID], entityID)
			self.grid[coords[0][coords[1]].coords = coords
		elif itemID > 0:
			self.grid[coords[0][coords[1]] = ch.Monster(Map.mapItemIDs[itemID], entityID)
			self.grid[coords[0][coords[1]].coords = coords

