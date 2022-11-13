import pickle as pkl
import characters as ch
import objects as ob


class MapGen:
	def __init__(self, number, size):
		self.mapGrid = [[0 for _ in range(size[1])] for _ in range(size[0])]

		self.charGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		self.objGrid = [[None for _ in range(size[1])] for _ in range(size[0])]
		self.itemGrid = [[None for _ in range(size[1])] for _ in range(size[0])]

		self.spwnList = []

		self.fileNameMap = f'maps/map{number}.pkl'
		self.fileNameChar = f'maps/map{number}_characters.pkl'
		self.fileNameItem = f'maps/map{number}_items.pkl'
		self.fileNameObj = f'maps/map{number}_objects.pkl'
		self.fileNameSpwn = f'maps/map{number}_spwn.pkl'

	def addMonster(self, coords, name):
		creature = ch.Monster(name)
		creature.coords = coords
		self.charGrid[coords[0]][coords[1]] = creature
		return creature

	def addNPC(self, coords, name):
		creature = ch.NPC(name)
		creature.coords = coords
		self.charGrid[coords[0]][coords[1]] = creature
		return creature

	def addObject(self, coords, name):
		creature = ob.Object(name)
		creature.coords = coords
		self.objGrid[coords[0]][coords[1]] = creature
		return creature

	def addItem(self, coords, name):
		creature = ob.Item(name)
		creature.coords = coords
		self.itemGrid[coords[0]][coords[1]] = creature
		return creature

	def addWeapon(self, coords, name):
		creature = ob.Weapon(name)
		creature.coords = coords
		self.itemGrid[coords[0]][coords[1]] = creature
		return creature

	def addArmour(self, coords, name):
		creature = ob.Armour(name)
		creature.coords = coords
		self.itemGrid[coords[0]][coords[1]] = creature
		return creature

	def addSpawn(self, coordsTL, coordsBR):
		xleft = coordsTL[0]
		ytop = coordsTL[1]
		xright = coordsBR[0]
		ybottom = coordsBR[1]

		for x in range(xleft,xright+1):
			for y in range(ybottom, ytop+1):
				coords = (x,y)
				self.spwnList.append(coords)

	def save(self):
		pkl.dump(self.charGrid, open(self.fileNameChar, 'wb'))
		pkl.dump(self.mapGrid, open(self.fileNameMap, 'wb'))
		pkl.dump(self.itemGrid, open(self.fileNameItem, 'wb'))
		pkl.dump(self.objGrid, open(self.fileNameObj, 'wb'))
		pkl.dump(self.spwnList, open(self.fileNameSpwn, 'wb'))


chart = MapGen(1, (10, 10))

chart.addMonster((8, 8), 'orc')
chart.addMonster((9, 4), 'orc')

chart.addSpawn((0,7),(2,4))

chart.save()
