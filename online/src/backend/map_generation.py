import pickle as pkl
import characters as ch
import objects as ob

class MapGen:
	def __init__(self, number, size):
		self.mapGrid = [[0 for _ in range(size[1])] for _ in range(size[0])]
		self.entGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		self.fileNameMap = 'maps/map' + str(number) + '.pkl'
		self.fileNameEnt = 'maps/map' + str(number) + '_entities' + '.pkl'

	def addMonster(self, coords, name):
		creature = ch.Monster(name)
		creature.coords = coords
		self.entGrid[coords[0]][coords[1]] = creature
		return creature

	def addNPC(coords, name):
		creature = ch.NPC(name)
		creature.coords = coords
		self.entGrid[coords[0]][coords[1]] = creature
		return creature

	def addObject(coords, name):
		creature = ob.(name)
		creature.coords = coords
		self.entGrid[coords[0]][coords[1]] = creature
		return creature

	def save(self):
		pkl.dump(self.entGrid, open(self.fileNameEnt, 'wb'))
		pkl.dump(self.mapGrid, open(self.fileNameMap, 'wb'))

chart = MapGen(1,(10,10))

chart.addMonster((8,8), 'orc')
chart.addMonster((9,4), 'orc')

chart.save()