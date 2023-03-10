import pickle as pkl
import csv
import os

from typing import List, Dict, Tuple, Optional

class MapGen:
	def __init__(self, size: Tuple[int, int]):
		self.mapGrid = [[0 for _ in range(size[1])] for _ in range(size[0])]

		self.objects: List[Tuple[str, List[int]]] = []

		self.spawn: Dict[str, List[Tuple[int, int]]] = {
			'Player': [],
			'Monster': [],
			'NPC': []
		}

	def addObject(self, name: str, coords: List[int]):
		info = (name, coords)
		self.objects.append(info)

	def addSpawn(self, entity: str, coordsTL: Tuple[int, int], coordsBR: Optional[Tuple[int,int]]=None):
		if coordsBR is None:
			self.spawn[entity].append(coordsTL)
		else:
			xleft = coordsTL[0]
			ytop = coordsTL[1]
			xright = coordsBR[0]
			ybottom = coordsBR[1]

			for x in range(xleft,xright+1):
				for y in range(ybottom, ytop+1):
					coords = (x,y)
					self.spawn[entity].append(coords)

	def save(self, number: int):

		if not os.path.exists(f'./map{number}'):
			os.mkdir(f'./map{number}')
			open(f'map{number}/entities.csv', 'x')

			with open(f'map{number}/entities.csv', 'w') as file:
				csv_writer = csv.writer(file)
				csv_writer.writerow(['Monsters', 'NPCs'])

		file_name = {
			'Terrain': f'map{number}/terrain.pkl',
			'Objects': f'map{number}/objects.pkl',
			'NPC Spawn': f'map{number}/npc_spawn.pkl',
			'Monster Spawn': f'map{number}/monster_spawn.pkl',
			'Player Spawn': f'map{number}/player_spawn.pkl'
		}
		pkl.dump(self.spawn['Player'], open(file_name['Player Spawn'], 'wb'))
		pkl.dump(self.mapGrid, open(file_name['Terrain'], 'wb'))
		pkl.dump(self.spawn['Monster'], open(file_name['Monster Spawn'], 'wb'))
		pkl.dump(self.spawn['NPC'], open(file_name['NPC Spawn'], 'wb'))
		pkl.dump(self.objects, open(file_name['Objects'], 'wb'))


chart = MapGen((10, 10))

chart.addSpawn('Player', (0, 7), (2, 2))
chart.addSpawn('Monster', (8, 8), (9, 1))
chart.addSpawn('NPC', (2, 9), (4, 8))
chart.addSpawn('NPC', (2, 1), (4, 0))

chart.save(1)
