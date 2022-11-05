import pygame as pg
import numpy as np
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

class Cell:
    def __init__(self, counter, cellCoords, prevCoords = None):
        self.count = counter
        self.coords = cellCoords
        self.path = prevCoords
  
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
def accountTerrain(surface, coords):
    pixelColour = checkColour(surface, coords)
    if pixelColour == mountains:
        multiplier = 3
    elif pixelColour == hills:
        multiplier = 1.5
    elif pixelColour == forest:
        multiplier = 1.2
    elif pixelColour == marsh:
        multiplier = 2
    elif pixelColour == path:
        multiplier = 0.9
    else:
        multiplier = 1
    return multiplier

#Generates all cells on the surface
def generateCells(surface, startCoords):
    # rendCoords = endCoords
    # directions = [[0,-2], [2,-2], [2,0], [2,2], [0,2], [-2,2], [-2,0], [-2,-2]]
    # directions = [[0,-2], [2,0], [0,2], [-2,0]]
    directions = [[0,-2], [1,-2], [2,-2], [2,-1], [2,0], [2,1], [2,2], [1,2], [0,2], [-1,2], [-2,2], [-2,1], [-2,0], [-2,-1], [-2,-2], [-1,-2]]
    # directions = [[0,-2], [1,-2], [2,-1], [2,0], [2,1], [1,2], [0,2], [-1,2], [-2,1], [-2,0], [-2,-1], [-1,-2]]
    
    width, height = pg.Surface.get_size(surface)
    
    coords = [startCoords]
    cells = [[Cell(-1,(x,y)) for y in range(height)] for x in range(width)]
    
    cells[startCoords[0]][startCoords[1]].count = 0
    for currentCoords in coords:
        cCell = cell(cells, currentCoords)
        multiplier = accountTerrain(surface, currentCoords)
        for direction in directions:
            coord = tuple(np.add(currentCoords,direction))
            
            if coord[0] < 0 or coord[0] >= width or coord[1] < 0 or coord[1] >= height:
                continue
            if checkColour(surface, coord) == water:
                continue
            
            nCell = cell(cells, coord)
            counter = cCell.count + multiplier*(direction[0]**2+direction[1]**2)**0.5
            
            if nCell.count > counter or nCell.count == -1:
                nCell.count = counter
                coords.append(coord)
                nCell.path = cCell
            
    return cells
    
def plotPath(surface, cells, endCoords):
    # rendCoords = [0,0]
    # for i,x in enumerate(endCoords):
    #     x = x - x%2
    #     rendCoords[i] = x
    # rendCoords = tuple(rendCoords)
    rendCoords = endCoords
    
    cell1 = cells[rendCoords[0]][rendCoords[1]]
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
    
    cells = generateCells(freshMapImg, (x1,y1))
    
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
            
        if pinToggle:
            xm, ym = pg.mouse.get_pos()
            display.blit(pinImg, (xm-int(pinWidth/2), ym-pinHeight))
        if pathToggle:
            display.blit(pinImg, (x2-int(pinWidth/2), y2-pinHeight))
            plotPath(display, cells, (x2,y2))
            
        pg.display.update()
        display.fill((0,0,0))
        clock.tick(tickRate)
    pg.quit()