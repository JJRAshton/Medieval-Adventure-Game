import pygame as pg
"""Allows the Displaying of Any Required Maps"""
"""the Interface and"""

imageDir = 'assets/images/'
elementDir = 'assets/elements/'

def createScaleMaps(mapImg, minHeight):
    n = 20
    
    (width, height) = pg.Surface.get_size(mapImg)
    minWidth = minHeight*width/height
    
    mapImgList = [0 for _ in range(n)]
    for scale in range(len(mapImgList)):
        factor = scale/n
        newWidth = int(width*factor+minWidth)
        newHeight = int(height*factor+minHeight)
        mapImgList[scale] = [pg.transform.scale(mapImg, (newWidth,newHeight)), [newWidth, newHeight]]
    
    return mapImgList
    
def travelMap():
    displayWidth, displayHeight = displaySize = 1200,800
    backgroundColour = (245,245,220)
    pg.init()
    display = pg.display.set_mode((displayWidth, displayHeight))
    display.fill(backgroundColour)
    clock = pg.time.Clock()
    tickRate = 60
    scrollSpeed = 1
    xc, yc = displayWidth/2, displayHeight/2
    
    xo, yo = 0, 0
    xs, ys = 0, 0
    scale = 1
    xm, ym = 0, 0
    
    mapName = 'ME_map'
    map_str = mapName+'.png'
    mapImg = pg.image.load(imageDir+map_str)
    mapWidth, mapHeight = mapSize = pg.Surface.get_size(mapImg)
    
    imgMaps = createScaleMaps(mapImg, displayHeight)
    
    closed = False
    while not closed:
        imageWidth = imgMaps[scale-1][1][0]
        imageHeight = imgMaps[scale-1][1][1]
        
        img = imgMaps[scale-1][0]
        factor = (scale-1)/20
        #For zoom on centre of screen
        xs = int((xc-xo)*mapWidth*factor/displayWidth)
        ys = int((yc-yo)*mapHeight*factor/displayHeight)
        
        xImage, yImage = xo-xs, yo-ys
        display.blit(img, (xImage, yImage))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                closed = True
            if event.type == pg.MOUSEWHEEL:
                if event.y == -1:
                    if scale > 1:
                        scale -= 1
                if event.y == 1:
                    if scale < 20:
                        scale += 1

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            if yImage-yc < 0:
                yo += scrollSpeed
        if keys[pg.K_DOWN]:
            if yImage-yc > -imageHeight:
                yo -= scrollSpeed
        if keys[pg.K_LEFT]:
            if xImage-xc < 0:
                xo += scrollSpeed
        if keys[pg.K_RIGHT]:
            if xImage-xc > -imageWidth:
                xo -= scrollSpeed
        
        pg.display.update()
        display.fill((0,0,0))
        clock.tick(tickRate)
    pg.quit()