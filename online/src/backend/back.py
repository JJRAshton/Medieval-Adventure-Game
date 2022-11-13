import pickle as pkl
from characters import Character, Player, NPC, Monster
import random as rd


# Gets the in game distance between two coords for attacks
def calcRadDist(coords1, coords2):
	xdiff = abs(coords2[0] - coords1[0])
	ydiff = abs(coords2[1] - coords1[1])

	maxdiff = max(xdiff, ydiff)
	dist = 5 * maxdiff

	return dist


# Gets the in game distance between two coords for travel
def calcPathDist(coords1, coords2):
	xdiff = abs(coords2[0] - coords1[0])
	ydiff = abs(coords2[1] - coords1[1])

	dist = 5 * (xdiff + ydiff)

	return dist


class Back:

	def __init__(self, mapLevel=1, nPlayers=1):
		self.map = mapLevel
		self.player_n = nPlayers

		self.terrainGrid = []

		self.characterGrid = []
		self.objectGrid = []
		self.itemGrid = []

		self.characters = []
		self.objects = []
		self.items = []

		self.players = []

		self.maxReach = 5

		self.loadMap()
		self.registerMapEntities()

		for _ in range(self.player_n):
			self.players.append(self.createPlayer())

	# Loads in the map from the map number given
	def loadMap(self):
		self.characterGrid = pkl.load(open(f'maps/map{self.map}_characters.pkl', 'rb'))
		self.objectGrid = pkl.load(open(f'maps/map{self.map}_objects.pkl', 'rb'))
		self.itemGrid = pkl.load(open(f'maps/map{self.map}_items.pkl', 'rb'))
		self.terrainGrid = pkl.load(open(f'maps/map{self.map}.pkl', 'rb'))
		self.spwnLoc = pkl.load(open(f'maps/map{self.map}_spwn.pkl', 'rb'))

	# Logs all entities on the starting map
	def registerMapEntities(self):

		charIDNum = 0
		itemIDNum = 0
		objIDNum = 0
		for y in range(len(self.characterGrid)):
			for x in range(len(self.characterGrid[0])):
				character = self.characterGrid[x][y]
				if character is None:
					continue
				else:
					character.id = charIDNum
					if character.reach > self.maxReach:
						self.maxReach = character.reach
					self.characters.append(character)
					charIDNum += 1
					if character.primaryWeapon is not None:
						character.primaryWeapon.id = itemIDNum
						self.items.append(character.primaryWeapon)
						itemIDNum += 1
					if character.armour is not None:
						character.armour.id = itemIDNum
						self.items.append(character.armour)
						itemIDNum += 1
					for item in character.inventory:
						item.id = itemIDNum
						self.items.append(item)
						itemIDNum += 1

		for y in range(len(self.itemGrid)):
			for x in range(len(self.itemGrid[0])):
				item = self.itemGrid[x][y]
				if item is None:
					continue
				else:
					item.id = itemIDNum
					self.items.append(item)
					itemIDNum += 1

		for y in range(len(self.objectGrid)):
			for x in range(len(self.objectGrid[0])):
				entity = self.objectGrid[x][y]
				if entity is None:
					continue
				else:
					entity.id = objIDNum
					self.objects.append(entity)
					objIDNum += 1

	# Creates a player and registers it
	def createPlayer(self):
		player = Player()

		charIDNum = len(self.characters)
		itemIDNum = len(self.items)

		player.id = charIDNum
		self.characters.append(player)

		if player.reach > self.maxReach:
			self.maxReach = player.reach

		charIDNum += 1
		if player.primaryWeapon is not None:
			player.primaryWeapon.id = itemIDNum
			self.items.append(player.primaryWeapon)
			itemIDNum += 1
		if player.armour is not None:
			player.armour.id = itemIDNum
			self.items.append(player.armour)
			itemIDNum += 1
		for item in player.inventory:
			item.id = itemIDNum
			self.items.append(item)
			itemIDNum += 1

		rand_index = rd.randint(1,len(self.spwnLoc))
		spwn_coords = self.spwnLoc.pop(rand_index)

		player.coords = spwn_coords
		self.characterGrid[spwn_coords[0]][spwn_coords[1]] = player
			
		return player

	# Moves a character on the grid
	def moveCharacter(self, charID, newCoords):
		character = self.characters[charID]
		prevCoords = character.coords
		vector = (newCoords[0]-prevCoords[0], newCoords[1]-prevCoords[1])

		character.move(vector)

		self.characterGrid[newCoords[0]][newCoords[1]] = character
		self.characterGrid[prevCoords[0]][prevCoords[1]] = None

	# Moves a character on the grid
	def moveObject(self, objID, newCoords):
		entity = self.objects[objID]
		prevCoords = entity.coords
		vector = (newCoords[0]-prevCoords[0], newCoords[1]-prevCoords[1])

		entity.move(vector)

		self.objectGrid[newCoords[0]][newCoords[1]] = entity
		self.objectGrid[prevCoords[0]][prevCoords[1]] = None

	# Moves a character on the grid
	def moveItem(self, itemID, newCoords):
		item = self.items[itemID]
		prevCoords = item.coords
		vector = (newCoords[0]-prevCoords[0], newCoords[1]-prevCoords[1])

		item.move(vector)

		self.itemGrid[newCoords[0]][newCoords[1]] = item
		self.itemGrid[prevCoords[0]][prevCoords[1]] = None

	# Checks if coords are valid to move to
	def is_validCoords(self, newCoords):
		x, y = newCoords
		size = (len(self.characterGrid[0]), len(self.characterGrid))

		if x > size[0] or x < 0 or y > size[1] or y < 0:
			valid = False
		elif self.characterGrid[x][y] is not None:
			valid = False
		elif self.objectGrid[x][y] is not None:
			valid = False
		else:
			valid = True

		return valid

	# Checks if character has the movement to move to coords
	def is_validMovement(self, charID, newCoords):
		x, y = newCoords
		oldx, oldy = self.characters[charID].coords
		if self.characters[charID].movement < calcPathDist((oldx, oldy), (x, y)):
			valid = False
		else:
			valid = True

		return valid

	# Makes a list of characters that can make an opportunity attack upon given characters movement to the new coords
	def checkOpportunity(self, charID, newCoords):
		searchRadius = int(self.maxReach/5)
		oldx, oldy = self.characters[charID].coords

		characters = []

		for y in range(oldy-searchRadius, oldy+searchRadius+1):
			for x in range(oldx-searchRadius, oldx+searchRadius+1):
				if self.characterGrid[x][y] is not None:
					entity = self.characterGrid[x][y]
					if entity.is_conscious:
						if entity.reach != self.maxReach:
							olddist = calcRadDist((x, y), (oldx, oldy))
							if olddist > entity.reach:
								continue
						newdist = calcRadDist((x, y), newCoords)
						if newdist > entity.reach:
							characters.append(entity)

		return characters

	# Checks if an attack is valid
	def is_validAttack(self, atkID, defID, catDef):
		atkCoords = self.characters[atkID].coords
		radius = int(self.characters[atkID].reach/5)
		if catDef == 2:
			defx, defy = self.objects[defID].coords
		elif catDef == 1:
			defx, defy = self.characters[defID].coords
		else:
			raise ValueError

		xmin = atkCoords[0] - radius
		xmax = atkCoords[0] + radius
		ymin = atkCoords[1] - radius
		ymax = atkCoords[1] + radius

		if defx < xmin or defx > xmax or defy < ymin or defy > ymax:
			valid = False
		else:
			valid = True

		return valid
