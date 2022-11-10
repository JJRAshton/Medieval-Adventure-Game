import pickle as pkl
import characters as ch
import objects as ob

class MapGen:
	def __init__(self, number, size):
		self.mapGrid = [[0 for _ in range(size[1])] for _ in range(size[0])]

		self.charGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		self.objGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		self.itemGrid = [[None for _ in range(size[1])] for _ in range(size[0])]

		self.fileNameMap = 'maps/map' + str(number) + '.pkl'
		self.fileNameChar = 'maps/map' + str(number) + '_characters' + '.pkl'
		self.fileNameItem = 'maps/map' + str(number) + '_items' + '.pkl'
		self.fileNameObj = 'maps/map' + str(number) + '_objects' + '.pkl'

	def addMonster(self, coords, name):
		creature = ch.Monster(name)
		creature.coords = coords
		self.charGrid[coords[0]][coords[1]] = creature
		return creature

	def addNPC(coords, name):
		creature = ch.NPC(name)
		creature.coords = coords
		self.charGrid[coords[0]][coords[1]] = creature
		return creature

	def addObject(coords, name):
		creature = ob.Object(name)
		creature.coords = coords
		self.objGrid[coords[0]][coords[1]] = creature
		return creature

	def addItem(coords, name):
		creature = ob.Item(name)
		creature.coords = coords
		self.itemGrid[coords[0]][coords[1]] = creature
		return creature

	def addWeapon(coords, name):
		creature = ob.Weapon(name)
		creature.coords = coords
		self.itemGrid[coords[0]][coords[1]] = creature
		return creature

	def addArmour(coords, name):
		creature = ob.Armour(name)
		creature.coords = coords
		self.itemGrid[coords[0]][coords[1]] = creature
		return creature

	def save(self):
		pkl.dump(self.charGrid, open(self.fileNameChar, 'wb'))
		pkl.dump(self.mapGrid, open(self.fileNameMap, 'wb'))
		pkl.dump(self.itemGrid, open(self.fileNameItem, 'wb'))
		pkl.dump(self.objGrid, open(self.fileNameObj, 'wb'))

chart = MapGen(1,(10,10))

chart.addMonster((8,8), 'orc')
chart.addMonster((9,4), 'orc')

chart.save()