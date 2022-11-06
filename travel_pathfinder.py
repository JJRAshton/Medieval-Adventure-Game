import pygame as pg
import numpy as np
from map_preload_pkl import Map
from sortedcontainers import SortedList
# import travel_visualiser as tv
"""Finds the Path Between Two Points On a Given Map"""

imageDir = 'assets/images/'
elementDir = 'assets/elements/'

#Calculates the distance between two cells
def calcDist(cell1, cell2):
    dist = np.linalg.norm(np.subtract(cell1.coords,cell2.coords))
    return dist

class Travel:
    def __init__(self):
        self.path = False
        self.nopath = False
        self.boat = False
        
        self.w = 1.2
        
        self.startCoords = (0,0)
        self.endCoords = (0,0)
        
    #Generates all cells on the surface with paths
    def generate(self, pMap):
        goalCell = pMap.getCell(self.endCoords)
        startCell = pMap.getCell(self.startCoords)
        
        startCell.count = 0
        startCell.f = 100000000
        pMap.editedCells.append(startCell)
        
        search_list = [pMap.getCell(self.startCoords)]
        
        frontier_list = SortedList()

        # This is a little bit whacky, search_list gets modified while being iterated through
        for searchCell in search_list:
                        
            for i, neighbouringCell in enumerate(searchCell.nbour):
                
                if not self.boat:
                    if neighbouringCell.terrain == pMap.water:
                        continue
                
                counter = searchCell.count + searchCell.terrain_multiplier*searchCell.nDist[i]
                    
                if neighbouringCell.count > counter or neighbouringCell.count == -1:
                    neighbouringCell.count = counter
                    pMap.editedCells.append(neighbouringCell)
                    neighbouringCell.path = searchCell
                    
                    h = self.w*calcDist(neighbouringCell, goalCell)
                    g = neighbouringCell.count
                    
                    distanceToEndEstimate = h + g
                    neighbouringCell.distanceToEndEstimate = distanceToEndEstimate
                    frontier_list.add(neighbouringCell)
              
            if len(frontier_list) != 0:
                search_list.append(frontier_list.pop(0))
            
            if searchCell.coords == self.endCoords:
                break
        
        print('Path Generated!')

    #Plots path across the map    
    def plot(self, pMap):
        cell1 = pMap.getCell(self.endCoords)
        while cell1.count != 0:
            cell2 = cell1.path
            pg.draw.line(pMap.map, pMap.path, cell1.coords, cell2.coords)
            cell1 = cell2
    
def testMap():
    displayWidth, displayHeight = displaySize = 1200,800
    backgroundColour = (245,245,220)
    pg.init()
    display = pg.display.set_mode((displayWidth, displayHeight))
    display.fill(backgroundColour)
    clock = pg.time.Clock()
    tickRate = 60
    
    mapName = 'Test_map'
    map_str = mapName+'.png'
    mapImg = pg.image.load(imageDir+map_str).convert_alpha()
    
    pinName = 'pin1'
    pin_str = pinName + '.png'
    pinImg = pg.image.load(elementDir+pin_str).convert_alpha()
    pinWidth, pinHeight = pinSize = pg.Surface.get_size(pinImg)
    
    xImage, yImage = 0, 0
    xm, ym = 0, 0
    
    mMap = Map(mapImg, mapName)
    path = Travel()
    
    startPin = False
    endPin = False
    generated = False
    closed = False
    while not closed:
        display.blit(mapImg, (xImage, yImage))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                closed = True
                
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            path.generate(mMap)
            generated = True
        if keys[pg.K_1]:
            generated = False
            path.startCoords = pg.mouse.get_pos()
            startPin = True
        if keys[pg.K_2]:
            generated = False
            path.endCoords = pg.mouse.get_pos()
            endPin = True
 
        if startPin:
            display.blit(pinImg, (path.startCoords[0]-int(pinWidth/2), path.startCoords[1]-pinHeight))
        if endPin:
            display.blit(pinImg, (path.endCoords[0]-int(pinWidth/2), path.endCoords[1]-pinHeight))
        if generated:
            path.plot(mMap)
            
        pg.display.update()
        display.fill((0,0,0))
        clock.tick(tickRate)
    pg.quit()