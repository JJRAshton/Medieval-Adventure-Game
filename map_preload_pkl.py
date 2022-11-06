import pygame as pg
from os import path
import pickle as pkl

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
        
        # self.directions = [(0,-1), (1,-2), (1,-1), (2,-1), (1,0), (2,1), (1,1), (1,2), (0,1), (-1,2), (-1,1), (-2,1), (-1,0), (-2,-1), (-1,-1), (-1,-2)]
        self.directions = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]

        self.dirN = len(self.directions)
        
        self.editedCells = []
        
        self.receiveCells()
        
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
    
    #Generates the cells for path finding without neighbours
    def generateCells(self):
        
        # Calculating the absolute distances per direction once to save work
        dirAbs = {direction: (direction[0]**2+direction[1]**2)**0.5 for direction in self.directions}
        
        for y in range(self.height):
            for x in range(self.width):
                for direction in self.directions:
                    coord = (x + direction[0], y + direction[1])
                    
                    if coord[0] < 0 or coord[0] >= self.width or coord[1] < 0 or coord[1] >= self.height:
                        continue
                    
                    terrain = self.checkColour(coord)
                    currentCell = self.getCell(coord)
                    currentCell.terrain = terrain
                    currentCell.terrain_multiplier = self.accountTerrain(terrain)
                    
                    currentCell.nDist.append(dirAbs[direction])
                    
        print('Cells Generated')
    
    #Adds neighbours to cells
    def addNeighbours(self):
        for y in range(self.height):
            for x in range(self.width):
                for direction in self.directions:
                    coord = (x + direction[0], y + direction[1])
                    
                    if coord[0] < 0 or coord[0] >= self.width or coord[1] < 0 or coord[1] >= self.height:
                        continue
                    
                    currentCell = self.getCell(coord)
                    neighbouringCell = self.getCell((x, y))
                    currentCell.nbour.append(neighbouringCell)
                    
    #Gets the pregenerated cells from the local file
    def recallCells(self, fileDir):
        self.cells = pkl.load(open(fileDir,'rb'))
        self.addNeighbours()
        print('Cells Received')
    
    #Stores generated cells in local file
    def storeCells(self, fileDir):
        pkl.dump(self.cells, open(fileDir,'wb'))
        print('Cells Stored')
        
    #Gets and stores the cells
    def receiveCells(self):
        self.cells = [[Cell(-1,(x,y)) for y in range(self.height)] for x in range(self.width)]
        
        fileLoc = 'assets/pregen_maps/'
        fileDir = fileLoc + self.name + str(self.dirN) + '.pkl'
        
        if path.isfile(fileDir):
            self.recallCells(fileDir)
        else:
            self.generateCells()
            self.storeCells(fileDir)
            self.addNeighbours()
            
    #Resets the cells' count
    def resetCells(self):
        for cell in self.editedCells:
            cell.count = -1
            cell.path = None
        
        self.editedCells = []
        print('Cells Reset')
        