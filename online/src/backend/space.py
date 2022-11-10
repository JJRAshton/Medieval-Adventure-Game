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
		objIDNum = 0
		for y in range(len(self.characterGrid)):
			for x in range(len(self.characterGrid[0])):
				character = characterGrid[x][y]
				if character == None:
					continue
				else:
					character.id = charIDNum
					if character.reach > self.maxReach: self.maxReach = character.reach
					self.characters.append(character)
					charIDNum += 1
					if character.primaryWeapon != None: 
						character.primaryWeapon.id = itemIDNum
						self.item.append(character.primaryWeapon)
						itemIDNum += 1
					if character.armour != None: 
						character.armour.id = itemIDNum
						self.item.append(character.armour)
						itemIDNum += 1
					for item in character.inventory:
						item.id = itemIDNum
						self.item.append(item)
						itemIDNum += 1

		for y in range(len(self.itemGrid)):
			for x in range(len(self.itemGrid[0])):
				item = itemGrid[x][y]
				if item == None:
					continue
				else:
					item.id = itemIDNum
					self.items.append(item)
					itemIDNum += 1

		for y in range(len(self.objectGrid)):
			for x in range(len(self.objectGrid[0])):
				entity = objectGrid[x][y]
				if entity == None:
					continue
				else:
					entity.id = objIDNum
					self.objects.append(entity)
					objIDNum += 1

	#Moves a character on the grid
	def moveCharacter(self, charID, newCoords):
		character = self.characters[charID]
		prevCoords = character.coords
		vector = (newCoords[0]-prevCoords[0],newCoords[1]-prevCoords[1])

		character.move(vector)

		self.characterGrid[newCoords[0]][newCoords[1]] = character
		self.characterGrid[prevCoords[0]][prevCoords[1]] = None

	#Moves a character on the grid
	def moveObject(self, objID, newCoords):
		entity = self.objects[objID]
		prevCoords = entity.coords
		vector = (newCoords[0]-prevCoords[0],newCoords[1]-prevCoords[1])

		entity.move(vector)

		self.entityGrid[newCoords[0]][newCoords[1]] = entity
		self.entityGrid[prevCoords[0]][prevCoords[1]] = None

	#Moves a character on the grid
	def moveItem(self, itemID, newCoords):
		item = self.items[itemID]
		prevCoords = item.coords
		vector = (newCoords[0]-prevCoords[0],newCoords[1]-prevCoords[1])

		item.move(vector)

		self.itemGrid[newCoords[0]][newCoords[1]] = item
		self.itemGrid[prevCoords[0]][prevCoords[1]] = None

	#Gets the in game distance between two coords for attacks
	def calcRadDist(coords1, coords2):
		xdiff = abs(coords2[0]-coords1[0])
		ydiff = abs(coords2[1]-coords1[1])
		
		maxdiff = max(xdiff,ydiff)
		dist = 5*maxdiff

		return dist

	#Gets the in game distance between two coords for travel
	def calcPathDist(coords1, coords2):
		xdiff = abs(coords2[0]-coords1[0])
		ydiff = abs(coords2[1]-coords1[1])

		dist = 5*(xdiff + ydiff)

		return dist

	#Checks if coords are valid to move to
	def is_validCoords(self, newCoords):
		x, y = newCoords
		size = (len(self.characterGrid[0]),len(self.characterGrid))

		if x > size[0] or x < 0 or y > size[1] or y < 0:
			valid = False
		elif self.characterGrid[x][y] != None:
			valid = False
		elif self.objectGrid[x][y] != None:
			valid = False
		else:
			valid = True

		return valid

	#Checks if character has the movement to move to coords
	def is_validMovement(self, charID, newCoords):
		x, y = newCoords
		oldx, oldy = self.characters[charID].coords
		if self.characters[charID].movement < calcPathDist((oldx,oldy), (x,y)):
			valid = False
		else:
			valid = True

		return valid

	#Makes a list of characters that can make an opportunity attack upon given characters movement to the new coords
	def checkOpportunity(self, charID, newCoords):
		searchRadius = int(self.maxReach/5)
		oldx, oldy = self.characters[charID].coords

		characters = []

		for y in range(oldy-searchRadius, oldy+searchRadius+1):
			for x in range(oldx-searchRadius, oldx+searchRadius+1):
				if self.characterGrid[x][y] != None:
					entity = self.characterGrid[x][y]
					if entity.is_conscious:
						if entity.reach != self.maxReach:
							olddist = self.calcRadDist((x,y),(oldx,oldy))
							if olddist > entity.reach:
								continue
						newdist = self.calcRadDist((x,y),newCoords)
						if newdist > entity.reach:
							characters.append(entity)

		return characters

	#Checks if an attack is valid
	def is_validAttack(self, atkID, defID):
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