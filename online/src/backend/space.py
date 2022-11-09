import pickle as pkl

class Chart:
	def __init__(self, mapNumber):
		self.map = mapNumber

		self.terrainGrid = []

		self.entityGrid = []
		self.entities = []

		self.getMap()

	#Loads in the map from the map number given
	def loadMap(self):
		self.entityGrid = pkl.load(open('maps/map'+str(self.map)+'_entities'+'.pkl','rb'))
		self.terrainGrid = pkl.load(open('maps/map'+str(self.map)+'.pkl','rb'))

	#Gives all entities ID numbers
	def idEntities(self):

		idNum = 0
		for y in range(len(self.entityGrid)):
			for x in range(len(self.entityGrid[0])):
				entity = entityGrid[x][y]
				if itemID == None:
					continue
				else:
					entity.id = idNum
					self.entities.append(entity)
					idNum += 1

	#Moves an entity on the grid
	def moveEntity(self, entID, newCoords):
		entity = self.entities[entID]
		prevCoords = entity.coords
		vector = (newCoords[0]-prevCoords[0],newCoords[1]-prevCoords[1])

		entity.move(vector)

		self.entityGrid[newCoords[0]][newCoords[1]] = entity
		self.entityGrid[prevCoords[0]][prevCoords[1]] = None

	#Checks if a move is valid
	def validateMove(self, entID, newCoords):
		x, y = newCoords
		size = (len(self.entityGrid[0]),len(self.entityGrid))
		if x > size[0] or x < 0 or y > size[1] or y < 0:
			valid = False
		elif self.entityGrid[x][y] != None:
			valid = False
		else:
			valid = True

		return valid

	#Checks if an attack is valid
	def validateAttack(self, atkID, defID):
		atkCoords = self.entities[atkID].coords
		radius = self.entities[atkID].reach/5
		defx, defy = self.entities[defID].coords

		xmin = atkCoords[0] - radius
		xmax = atkCoords[0] + radius
		ymin = atkCoords[1] - radius
		ymax = atkCoords[1] + radius

		if defx < xmin or defx > xmax or defy < ymin or defy > ymax:
			valid = False
		else:
			valid = True

		return valid