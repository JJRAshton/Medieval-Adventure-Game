import pygame as pg
"""Allows the usage of various interface elements"""

imageDir = 'assets/images/'
elementDir = 'assets/elements/'

class InputBox:
    def __init__(self, boxType, size, coords, text = None):
        self.btype = boxType
        self.size = self.width, self.height = size
        self.coords = self.x, self.y = coords
        self.active = False
        self.text = text
        
        self.colours = {}
        self.colours['default'] = (215,215,200)
        self.colours['pressed'] = (195,195,175)
        self.colours['font'] = (35,35,30)
        
        self.colour = self.colours['default']
        
        self.update()
        
    def update(self):
        self.rect = pg.Rect(self.coords, self.size)
        
    def draw(self, surface):
        #Create Box
        box = pg.Surface(self.size)
        box.fill(self.colour)
        
        if self.text != None:
            #Create Text
            font = 'timesnewroman'
            fontHeight = int(0.7*self.height)
            fontObj = pg.font.Font(pg.font.match_font(font), fontHeight)
            txt_surface = fontObj.render(self.text, True, self.colours['font'])
            
            box.blit(txt_surface, (10,int((self.height-fontHeight)*0.25)))
        
        surface.blit(box, self.coords)
        
        return surface
    
    def manageEvent(self, event):
        if self.btype == 'typing':
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    if self.text == None:
                        self.text = ''
                else:
                    self.active = False
                    if self.text == '':
                        self.text = None
            if self.active:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.active = False
                        if self.text == '':
                            self.text = None
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif pg.K_a <= event.key <= pg.K_z or pg.K_0 <= event.key <= pg.K_9:
                        self.text += chr(event.key)
            self.colour = self.colours['pressed'] if self.active else self.colours['default']
        elif self.btype == 'button':
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
        
def addStaticBox(surface, boxSize, coords, text = None, boxColour = (215,215,200)):
    width, height = boxSize
    box = pg.Surface(boxSize)
    
    box.fill(boxColour)
    
    if text != None:
        fontColour = (35,35,30)
        #Create Text
        font = 'timesnewroman'
        fontHeight = int(0.7*height)
        fontObj = pg.font.Font(pg.font.match_font(font), fontHeight)
        txt_surface = fontObj.render(text, True, fontColour)
            
        box.blit(txt_surface, (15,int((height-fontHeight)*0.25)))
    
    surface.blit(box, coords)
    
    return surface

class DynamicTable:
    def __init__(self, tableCol, coords):
        self.x, self.y = self.coords = coords
        self.cols = tableCol
        
        self.boxHeight = 40
        self.textBoxSize = 200, self.boxHeight
        self.numBoxSize = 100, self.boxHeight
        self.sep = 20
        self.nRows = 1
        
        self.textBoxes = [[] for _ in range(len(self.cols))]
        self.tableWidth = -self.sep
        x = self.x
        y = self.y + self.boxHeight + self.sep
        for col, heading in enumerate(self.cols):
            if self.cols[heading] == 'number':
                self.tableWidth += self.numBoxSize[0] + self.sep
                box = InputBox('typing', self.numBoxSize, (x,y))
                self.textBoxes[col].append(box)
                x += self.numBoxSize[0] + self.sep
            elif self.cols[heading] == 'text':
                self.tableWidth += self.textBoxSize[0] + self.sep
                box = InputBox('typing', self.textBoxSize, (x,y))
                self.textBoxes[col].append(box)
                x += self.textBoxSize[0] + self.sep
                
        self.extendButton = InputBox('button', (self.boxHeight, self.boxHeight), (0,0), '+')
        
        self.update()
        
    def update(self):
        self.tableHeight = (self.boxHeight + self.sep)*(self.nRows+1)
        
        buttonX = self.coords[0] + int(self.tableWidth/2) - int(self.boxHeight/2)
        buttonY = self.coords[1] + self.tableHeight
        buttonCoords = buttonX, buttonY
        self.extendButton.coords = buttonCoords
        self.extendButton.update()
        
    def addRow(self):
        self.nRows += 1
        
        for col in self.textBoxes:
            boxSize = col[-1].size
            boxX = col[-1].x
            boxY = col[-1].y + self.boxHeight + self.sep
            boxCoords = boxX, boxY
            box = InputBox('typing', boxSize, boxCoords)
            col.append(box)
        self.update()
        
    def draw(self, surface):
        #Add heading boxes
        x, y = self.coords
        for heading in self.cols:
            if self.cols[heading] == 'number':
                surface = addStaticBox(surface, self.numBoxSize, (x,y), heading)
                x += self.numBoxSize[0] + self.sep
            elif self.cols[heading] == 'text':
                surface = addStaticBox(surface, self.textBoxSize, (x,y), heading)
                x += self.textBoxSize[0] + self.sep
        
        #Add rows of typing boxes underneath
        for row in range(self.nRows):
            for col, heading in enumerate(self.cols):
                if self.cols[heading] == 'number':
                    surface = self.textBoxes[col][row].draw(surface)
                elif self.cols[heading] == 'text':
                    surface = self.textBoxes[col][row].draw(surface)
        
        #Add the button to the table
        surface = self.extendButton.draw(surface)
        
        return surface
    
    def manageEvent(self, event):
        for col in self.textBoxes:
            for box in col:
                box.manageEvent(event)
                
        self.extendButton.manageEvent(event)
        
        if self.extendButton.active:
            self.addRow()
            self.extendButton.active = False

class StaticTable:
    def __init__(self, tableCol, coords, contents):
        self.cols = tableCol
        self.coords = self.x, self.y = coords
        self.contents = contents
        
        self.boxHeight = 40
        self.textBoxSize = 200, self.boxHeight
        self.numBoxSize = 100, self.boxHeight
        self.sep = 20
    
    def getContents(self, table):
        
        nCols = len(table.textBoxes)
        nRows = [len(col) for col in table.textBoxes][0]
        self.contents = [['' for _ in range(nRows)] for _ in range(nCols)]
        
        for col in range(len(table.textBoxes)):
            for row in range(len(table.textBoxes[col])):
                self.contents[col][row] = table.textBoxes[col][row].text
        
    def draw(self, surface):
        #Add heading boxes
        x, y = self.coords
        for heading in self.cols:
            if self.cols[heading] == 'number':
                surface = addStaticBox(surface, self.numBoxSize, (x,y), heading)
                x += self.numBoxSize[0] + self.sep
            elif self.cols[heading] == 'text':
                surface = addStaticBox(surface, self.textBoxSize, (x,y), heading)
                x += self.textBoxSize[0] + self.sep
                
        for row in range(len(self.contents[0])):
            x = self.x
            y += self.boxHeight + self.sep
            for col, heading in enumerate(self.cols):
                if self.cols[heading] == 'number':
                    surface = addStaticBox(surface, self.numBoxSize, (x,y), self.contents[col][row])
                    x += self.numBoxSize[0] + self.sep
                elif self.cols[heading] == 'text':
                    surface = addStaticBox(surface, self.textBoxSize, (x,y), self.contents[col][row])
                    x += self.textBoxSize[0] + self.sep
                    
        return surface
            
class Screen:
    def __init__(self, screenSize, backgroundColour, nextButton = True):
        self.screenSize = screenSize
        self.bColour = backgroundColour
        self.elements = []
        
        self.screen = pg.Surface(self.screenSize)
        
        if nextButton:
            buttonCoords = (self.screenSize[0]-120, self.screenSize[1]-80)
            self.nextButton = InputBox('button', (80, 40), buttonCoords, 'Next')
            self.elements.append(self.nextButton)
        
    def draw(self, display):
        self.screen.fill(self.bColour)
        
        for element in self.elements:
            self.screen = element.draw(self.screen)
        
        display.blit(self.screen, (0,0))