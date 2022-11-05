import pygame as pg
from os import path

class Cell:
    def __init__(self, counter, cellCoords):
        self.count = counter
        self.coords = cellCoords
        self.path = None
        self.terrain = None
        self.terrain_multiplier = 1
        self.nbour = []
        self.nDist = []

    def __lt__(self, other):
        # Needed to make SortedList work
        return self.distanceToEndEstimate < other.distanceToEndEstimate

        
class Map:
    # Dictionary used to quickly lookup the multiplier for different terrrains
    terrainMultiplier = {
        (0,0,0): 3,         # mountains
        (150,150,150): 1.5, # hills
        (0,255,0): 1.2,     # forest
        (255,0,255): 2,     # marsh
        (255,0,0): 0.9      # path
    }

    def __init__(self, surface, mapname):
        self.mountains = (0,0,0)
        self.path = (255,0,0)
        self.forest = (0,255,0)
        self.water = (0,0,255)
        self.hills = (150,150,150)
        self.marsh = (255,0,255)
        self.plains = (255,255,255)
        
        self.map = surface
        self.width, self.height = pg.Surface.get_size(self.map)
        self.name = mapname
        
        self.cells = [[Cell(-1,(x,y)) for y in range(self.height)] for x in range(self.width)]
        self.generateCells()
        
    #Returns RGB of a surface at the given coords
    def checkColour(self, coords):
        r,g,b,a = self.map.get_at(coords)
        return (r,g,b)
    
    #Calculates the distance multiplier for the terrain
    def accountTerrain(self, terrain):
        return Map.terrainMultiplier[terrain] if terrain in Map.terrainMultiplier else 1
    
    #Returns the cell at the coords
    def getCell(self, coords):
        x, y = coords
        return self.cells[x][y]
    
    #Generates the cells for path finding
    def generateCells(self):
        directions = [(0,-2), (1,-2), (2,-1), (2,0), (2,1), (1,2), (0,2), (-1,2), (-2,1), (-2,0), (-2,-1), (-1,-2)]
        
        # Calculating the absolute distances per direction once to save work
        dirAbs = {direction: (direction[0]**2+direction[1]**2)**0.5 for direction in directions}
        
        for y in range(self.height):
            for x in range(self.width):
                for direction in directions:
                    coord = (x + direction[0], y + direction[1])
                    
                    if coord[0] < 0 or coord[0] >= self.width or coord[1] < 0 or coord[1] >= self.height:
                        continue
                    
                    terrain = self.checkColour(coord)
                    currentCell = self.getCell(coord)
                    currentCell.terrain = terrain
                    currentCell.terrain_multiplier = self.accountTerrain(terrain)
                    
                    neighbouringCell = self.getCell((x, y))
                    neighbouringCell.nbour.append(currentCell)
                    neighbouringCell.nDist.append(dirAbs[direction])
                    
        print('Cells Generated')
    
    #Gets the pregenerated cells from the local file
    # def recallCells(self, fileDir):
    #     self.cells = pkl.load(open(fileDir+'.p','rb'))
    #     print('Cells Received')
    
    #Stores generated cells in local file
    # def storeCells(self, fileDir):
    #     pkl.dump(self.cells, open(fileDir+'.p','wb'))
    #     print('Cells Stored')
        
    #Gets and stores the cells
    def receiveCells(self):
        self.cells = [[Cell(-1,(x,y)) for y in range(self.height)] for x in range(self.width)]
        
        fileLoc = 'assets/pregen_maps/'
        fileStr = fileLoc + self.name
        
        if path.isfile(fileStr):
            self.recallCells(fileStr)
        else:
            self.generateCells()
            # self.storeCells(fileStr)
            
    #Resets the cells' count
    def resetCells(self):
        print('Cells Reset')
        
        for y in range(self.height):
            for x in range(self.width):
                self.getCell((x,y)).count = -1
        