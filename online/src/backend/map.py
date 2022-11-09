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

		self.entityGrid = []
		self.entities = []

		self.getMap()

	#Loads in the map from the map number given
	def getMap(self):
		self.entityGrid = pkl.load(open('maps/map'+str(self.map)+'.pkl','rb'))

	#Gets what ID is in cell at given coords and places the relevant item
	def createEntity(self, coords, itemID):
		if itemID > 200:
			entity = ch.Object(Map.mapItemIDs[itemID])
		elif itemID > 100:
			entity = ch.NPC(Map.mapItemIDs[itemID])
		elif itemID > 0:
			entity = ch.Monster(Map.mapItemIDs[itemID])

		entity.coords = coords
		self.entityGrid[coords[0]][coords[1]] = entity

		return entity

	#Creates the map
	def create(self):

		idNum = 0
		for y in range(len(self.entityGrid)):
			for x in range(len(self.entityGrid[0])):
				itemID = self.entityGrid[coords[0]][coords[1]]
				if itemID == 0:
					continue
				else:
					entity = createEntity((x,y), itemID)
					entity.entityID = idNum
					self.entities.append(entity)
					idNum += 1