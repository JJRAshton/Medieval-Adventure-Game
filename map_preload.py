import pygame as pg
import numpy as np
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
        
class Map:
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
    
        self.receiveCells()
        
    #Returns RGB of a surface at the given coords
    def checkColour(self, coords):
        r,g,b,a = self.map.get_at(coords)
        return (r,g,b)
    
    #Calculates the distance multiplier for the terrain
    def accountTerrain(self, terrain):
        if terrain == self.mountains:
            multiplier = 3
        elif terrain == self.hills:
            multiplier = 1.5
        elif terrain == self.forest:
            multiplier = 1.2
        elif terrain == self.marsh:
            multiplier = 2
        elif terrain == self.path:
            multiplier = 0.9
        else:
            multiplier = 1
            
        return multiplier
    
    #Returns the cell at the coords
    def getCell(self, coords):
        x, y = coords
        cell = self.cells[x][y]
        return cell
    
    #Generates the cells for path finding
    def generateCells(self):
        directions = [[0,-2], [1,-2], [2,-1], [2,0], [2,1], [1,2], [0,2], [-1,2], [-2,1], [-2,0], [-2,-1], [-1,-2]]
        
        for y in range(self.height):
            for x in range(self.width):
                for direction in directions:
                    coord = tuple(np.add((x,y),direction))
                    
                    if coord[0] < 0 or coord[0] >= self.width or coord[1] < 0 or coord[1] >= self.height:
                        continue
                    
                    terrain = self.checkColour(coord)
                    self.getCell(coord).terrain = terrain
                    self.getCell(coord).terrain_multiplier = self.accountTerrain(terrain)
                    
                    self.getCell((x,y)).nbour.append(self.getCell(coord))
                    self.getCell((x,y)).nDist.append((direction[0]**2+direction[1]**2)**0.5)
                    
        print('Cells Generated')
    
    #Gets the pregenerated cells from the local file
    def recallCells(self, fileDir):
        print('Cells Received')
    
    #Stores generated cells in local file
    def storeCells(self, fileDir):
        print('Cells Stored')
        
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
        
        
        