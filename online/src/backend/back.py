import pickle as pkl
from characters import Character, Player, NPC, Monster
from objects import Object
import random as rd
import pandas as pd
import os


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
	maps_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..resources/inputs/maps'))

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
		self.monsters = []
		self.npcs = []

		self.maxReach = 5

		self.loadMap()
		self.addMapNPCs()

		for _ in range(self.player_n):
			self.players.append(self.createCharacter('Player'))

	# Loads in the map from the map number given
	def loadMap(self):
		map_dir = os.path.abspath(os.path.join(Back.maps_dir,f'map{self.map}'))

		self.terrainGrid = pkl.load(open(f'{map_dir}/terrain.pkl', 'rb'))
		size = (len(self.terrainGrid), len(self.terrainGrid[0]))

		self.characterGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		self.itemGrid = [[None for _ in range(size[1])] for _ in range(size[0])]

		self.objectGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		objectList = pkl.load(open(f'{map_dir}/objects.pkl', 'rb'))
		for object_info in objectList:
			name, coords = object_info
			self.objectGrid[coords[0]][coords[1]] = Object('name')

		self.spawn = {
			'Player': pkl.load(open(f'{map_dir}/player_spawn.pkl', 'rb')),
			'Monster': pkl.load(open(f'{map_dir}/monster_spawn.pkl', 'rb')),
			'NPC': pkl.load(open(f'{map_dir}/npc_spawn.pkl', 'rb'))
		}

	# Adds in the map NPCs
	def addMapNPCs(self):
		df = pd.read_csv(os.path.abspath(f'{Back.maps_dir}/map{self.map}/entities.csv'), keep_default_na=False)
		monster_list = [x for x in df['Monsters'] if x != '']
		npc_list = [x for x in df['NPCs'] if x != '']

		for monster_str in monster_list:
			self.monsters.append(self.createCharacter('Monster', monster_str))

		for npc_str in npc_list:
			self.npcs.append(self.createCharacter('NPC', npc_str))

	# Creates and registers a character and its inventory
	def createCharacter(self, character_type, sub_type=None):
		if character_type == 'Player' and sub_type is None:
			character = Player()
		elif character_type == 'Monster' and sub_type is not None:
			character = Monster(sub_type)
		elif character_type == 'NPC' and sub_type is not None:
			character = NPC(sub_type)
		else:
			raise ValueError

		charIDNum = len(self.characters)
		itemIDNum = len(self.items)

		character.id = charIDNum
		self.characters.append(character)

		if character.reach > self.maxReach:
			self.maxReach = character.reach

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

		rand_index = rd.randint(1, len(self.spawn[character_type]))
		spawn_coords = self.spawn[character_type].pop(rand_index)

		character.coords = spawn_coords
		self.characterGrid[spawn_coords[0]][spawn_coords[1]] = character

		return character

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
