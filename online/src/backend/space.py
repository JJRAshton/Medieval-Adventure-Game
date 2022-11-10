import pickle as pkl

class Chart:
	def __init__(self, mapNumber):
		self.map = mapNumber

		self.terrainGrid = []

		self.characterGrid = []
		self.objectGrid = []
		self.itemGrid = []

		self.characters = []
		self.objects = []
		self.items = []

		self.maxReach = 5

		self.getMap()

	#Loads in the map from the map number given
	def loadMap(self):
		self.characterGrid = pkl.load(open('maps/map'+str(self.map)+'_characters'+'.pkl','rb'))
		self.objectGrid = pkl.load(open('maps/map'+str(self.map)+'_objects'+'.pkl','rb'))
		self.itemGrid = pkl.load(open('maps/map'+str(self.map)+'_items'+'.pkl','rb'))
		self.terrainGrid = pkl.load(open('maps/map'+str(self.map)+'.pkl','rb'))

	#Logs all entities on the starting map
	def registerEntities(self):

		charIDNum = 0
		itemIDNum = 0
		for y in range(len(self.terrainGrid)):
			for x in range(len(self.terrainGrid[0])):
				character = characterGrid[x][y]
				if itemID == None:
					continue
				else:
					character.id = idNum
					if character.reach > self.maxReach: self.maxReach = character.reach
					self.characters.append(character)
					idNum += 1
					if character.primaryWeapon != None: 
						character.primaryWeapon.id = itemIDNum
						self.item.append(character.primaryWeapon)
						itemIDNum += 1
					if character.armour != None: 
						character.armour.id = itemIDNum
						self.item.append(character.armour)
						itemIDNum += 1
					

	#Moves an entity on the grid
	def moveEntity(self, entID, newCoords):
		entity = self.characters[entID]
		prevCoords = entity.coords
		vector = (newCoords[0]-prevCoords[0],newCoords[1]-prevCoords[1])

		entity.move(vector)

		self.entityGrid[newCoords[0]][newCoords[1]] = entity
		self.entityGrid[prevCoords[0]][prevCoords[1]] = None

	#Gets the in game distance between two coords
	def calcDist(coords1, coords2):
		xdiff = abs(coords2[0]-coords1[0])
		ydiff = abs(coords2[1]-coords1[1])
		
		maxdiff = max(xdiff,ydiff)
		dist = 5*maxdiff

		return dist

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

	#Makes a list of characters that can make an opportunity attack
	def checkOpportunity(self, entID, newCoords):
		searchRadius = int(self.maxReach/5)
		oldx, oldy = self.entities[entID].coords

		characters = []

		for y in range(oldy-searchRadius, oldy+searchRadius+1):
			for x in range(oldx-searchRadius, oldx+searchRadius+1):
				if self.entityGrid[x][y] != None:
					entity = self.entityGrid[x][y]
					if not hasattr(entity, 'conscious'):
						continue
					if entity.conscious:
						if entity.reach != self.maxReach:
							olddist = self.calcDist((x,y),(oldx,oldy))
							if olddist > entity.reach:
								continue
						newdist = self.calcDist((x,y),newCoords)
						if newdist > entity.reach:
							characters.append(entity)

		return characters

	#Checks if an attack is valid
	def validateAttack(self, atkID, defID):
		atkCoords = self.entities[atkID].coords
		radius = int(self.entities[atkID].reach/5)
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