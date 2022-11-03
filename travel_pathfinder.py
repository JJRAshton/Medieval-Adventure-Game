import pygame as pg
import numpy as np
from math import cos, sin
# import travel_visualiser as tv
"""Finds the Path Between Two Points On a Given Map"""

imageDir = 'assets/images/'
elementDir = 'assets/elements/'

mountains = (0,0,0)
path = (255,0,0)
forest = (0,255,0)
water = (0,0,255)
hills = (150,150,150)
marsh = (255,0,255)
plains = (255,255,255)

class Cell:
    def __init__(self, counter, cellCoords):
        self.count = counter
        self.coords = cellCoords
        self.path = None
        self.terrain = None
        self.nbour = []
        self.nDist = []
  
#Returns the cell at the coords
def cell(cells, coords):
    x, y = coords
    cell = cells[x][y]
    return cell

#Returns RGB of a surface at the given coords
def checkColour(surface, coords):
    r,g,b,a = surface.get_at(coords)
    return (r,g,b)

#Calculates the distance multiplier for the terrain
def accountTerrain(surface, terrain):
    if terrain == mountains:
        multiplier = 3
    elif terrain == hills:
        multiplier = 1.5
    elif terrain == forest:
        multiplier = 1.2
    elif terrain == marsh:
        multiplier = 2
    elif terrain == path:
        multiplier = 0.9
    else:
        multiplier = 1
    return multiplier

#Calculates the distance between two cells
def calcDist(cell1, cell2):
    dist = np.linalg.norm(np.subtract(cell1.coords,cell2.coords))
    return dist

#Generates the cells before path finding
def generateCells(surface):
    directions = [[0,-2], [1,-2], [2,-1], [2,0], [2,1], [1,2], [0,2], [-1,2], [-2,1], [-2,0], [-2,-1], [-1,-2]]
    
    width, height = pg.Surface.get_size(surface)
    cells = [[Cell(-1,(x,y)) for y in range(height)] for x in range(width)]
    
    for y in range(height):
        for x in range(width):
            for direction in directions:
                coord = tuple(np.add((x,y),direction))
                
                if coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord[1] >= height:
                    continue
                cell(cells, coord).terrain = checkColour(surface, coord)
                cell(cells,(x,y)).nbour.append(cell(cells, coord))
                cell(cells,(x,y)).nDist.append((direction[0]**2+direction[1]**2)**0.5)
    print('Cells Generated!')
    return cells

#Generates all cells on the surface with paths
def generatePath(surface, baseCells, startCoords, goalCoords):
    w = 1
    
    cells = baseCells
    goalCell = cell(cells,goalCoords)
    width, height = pg.Surface.get_size(surface)
    
    cell(cells, startCoords).count = 0
    frontier_list = [cell(cells, startCoords)]
    
    f_list = []
    for cCell in frontier_list:
        # multiplier = accountTerrain(surface, cCell.terrain)
        multiplier = 1
                    
        for i, nCell in enumerate(cCell.nbour):
            
            if nCell.terrain == water:
                continue
        
            counter = cCell.count + multiplier*nCell.nDist[i]
            
            if nCell.count > counter or nCell.count == -1:
                nCell.count = counter
                nCell.path = cCell
                frontier_list.append(nCell)
            
                h = w*calcDist(nCell, goalCell)
                g = nCell.count
                
                f = h + g
                
                f_list.append(f)
        cellweightings
          
    return cells
    
def plotPath(surface, cells, endCoords):
    cell1 = cell(cells, endCoords)
    while cell1.count != 0:
        cell2 = cell1.path
        pg.draw.line(surface, path, cell1.coords, cell2.coords)
        cell1 = cell2
    
    return surface
    
def testMap():
    displayWidth, displayHeight = displaySize = 1200,800
    backgroundColour = (245,245,220)
    pg.init()
    display = pg.display.set_mode((displayWidth, displayHeight))
    display.fill(backgroundColour)
    clock = pg.time.Clock()
    tickRate = 60
    
    x1, y1 = 50, 100
    x2, y2 = 600, 500
    
    mapName = 'Test_map'
    map_str = mapName+'.png'
    freshMapImg = pg.image.load(imageDir+map_str).convert_alpha()
    
    pinName = 'pin1'
    pin_str = pinName + '.png'
    pinImg = pg.image.load(elementDir+pin_str).convert_alpha()
    pinWidth, pinHeight = pinSize = pg.Surface.get_size(pinImg)
    
    xImage, yImage = 0, 0
    xm, ym = 0, 0
    
    baseCells = generateCells(freshMapImg)
    
    pinToggle = False
    pathToggle = False
    generated = False
    closed = False
    while not closed:
        mapImg = freshMapImg
        mapImg.blit(pinImg, (x1-int(pinWidth/2), y1-pinHeight))
        display.blit(mapImg, (xImage, yImage))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                closed = True
            if event.type == pg.MOUSEBUTTONDOWN:
                pathToggle = False
                generated = False
                pinToggle = True
            if event.type == pg.MOUSEBUTTONUP:
                pinToggle = False
                x2, y2 = xm, ym
                pathToggle = True
                
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            cells = generatePath(freshMapImg, baseCells, (x1,y1), (x2,y2))
            generated = True
            
        if pinToggle:
            xm, ym = pg.mouse.get_pos()
            display.blit(pinImg, (xm-int(pinWidth/2), ym-pinHeight))
        if pathToggle:
            display.blit(pinImg, (x2-int(pinWidth/2), y2-pinHeight))
            if generated:
                plotPath(display, cells, (x2,y2))
            
        pg.display.update()
        display.fill((0,0,0))
        clock.tick(tickRate)
    pg.quit()