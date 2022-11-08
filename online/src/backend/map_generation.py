import pickle as pkl

def generateMap(number):
	grid = [[0 for _ in range(10)] for _ in range(10)]

	grid[8][8] = 1
	grid[9][3] = 1

	fileName = 'maps/map' + str(number) + '.pkl'

	return grid, fileName

grid, fileName = generateMap(1)
pkl.dump(grid, open(fileName, 'wb'))