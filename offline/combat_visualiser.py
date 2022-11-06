import pygame as pg
import interface_elements as ie
import combat_calculator as cc
"""Allows the Displaying of Combat Interface"""

imageDir = 'assets/images/'
elementDir = 'assets/elements/'

def extractTable(table):
    
    outDict = {}
    for i in range(len(table.textBoxes[0])):
        name = table.textBoxes[0][i].text
        outDict[name] = []
        for j, col in enumerate(table.textBoxes):
            if j != 0:
                content = col[i].text
                if content != None:
                    while content[-1] == ' ':
                        content = content[:-1]
                    if content.isdigit():
                        outDict[name].append(int(content))
                    else:
                        outDict[name].append(content)
                else:
                    outDict[name].append(content)
    
    return outDict

def placeText(text, size, coords, surface):
    
    font = 'timesnewroman'
    fontHeight = size
    fontObj = pg.font.Font(pg.font.match_font(font), fontHeight)
    txt_surface = fontObj.render(text, True, (35,35,30))
    
    surface.blit(txt_surface, coords)
    
    return surface
            
def checkRepeats(creatureGroups, rolls, Screen, display):
    closed = False
    
    for r1, group1 in enumerate(creatureGroups):
        for r2, group2 in enumerate(creatureGroups):
            if r1 == r2 or creatureGroups[group1][0].ctype != 'player' or creatureGroups[group2][0].ctype == 'player':
                continue
            if rolls[r1] == rolls[r2]:
                button1 = ie.InputBox('button', (100, 40), (800, 400), group1)
                button2 = ie.InputBox('button', (100, 40), (1000, 400), group2)
                Screen.elements.append(button1)
                Screen.elements.append(button2)
                text1 = group1+' has the same roll as '+group2
                text2 = 'Which group to go first?'
                loop = True
                while loop:
                    Screen.draw(display)
                    display = placeText(text1, 20, (800, 300), display)
                    display = placeText(text2, 20, (850, 350), display)
                    pg.display.update()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            closed = True
                            return rolls, closed
                        for element in Screen.elements:
                            if hasattr(element,'manageEvent'):
                                element.manageEvent(event)
                        if button1.active:
                            rolls[r1] += 0.2
                            loop = False
                        elif button2.active:
                            rolls[r2] += 0.2
                            loop = False
                Screen.elements = Screen.elements[:-2]
    
    return rolls, closed

def combatInputs():
    #Display settings
    displayWidth, displayHeight = displaySize = 1200,800
    backgroundColour = (250,250,240)
    pg.init()
    clock = pg.time.Clock()
    tickRate = 60
    currentScreen = 1
    nScreens = 3
    screens = []
    
    #Creature Parameter Screen
    creatureParams = ie.Screen(displaySize, backgroundColour)
    
    cols = {'Name': 'text', 'Creature type': 'text', 'Number': 'number', 'Groups': 'number', 'Team': 'text'}
    tableCoords = (50, 100)
    creatureTable = ie.DynamicTable(cols, tableCoords)
    
    creatureParams.elements.append(creatureTable)
    
    #Player Rolls Screen
    playerRolls = ie.Screen(displaySize, backgroundColour)
    
    cols = {'Player': 'text', 'Roll': 'number'}
    tableCoords = (400, 100)
    playerRollTable = ie.DynamicTable(cols, tableCoords)
    
    playerRolls.elements.append(playerRollTable)
    
    #All Creature Rolls Screen
    allRolls = ie.Screen(displaySize, backgroundColour)
    
    cols = {'Player': 'text', 'Roll': 'number'}
    tableCoords = (100, 100)
    rollTable1 = ie.StaticTable(cols, tableCoords, [])
    
    cols = {'Creature': 'text', 'Roll': 'number'}
    tableCoords = (450, 100)
    rollTable2 = ie.StaticTable(cols, tableCoords, [])
    
    allRolls.elements.append(rollTable1)
    allRolls.elements.append(rollTable2)
    #Add screens to list
    screens.append(creatureParams)
    screens.append(playerRolls)
    screens.append(allRolls)
    
    display = pg.display.set_mode(screens[currentScreen-1].screenSize)
    closed = False
    while not closed:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                closed = True
            for element in screens[currentScreen-1].elements:
                if hasattr(element,'manageEvent'):
                    element.manageEvent(event)
            if screens[currentScreen-1].nextButton.active and currentScreen < nScreens:
                screens[currentScreen-1].nextButton.active = False
                currentScreen += 1
                
                #Creates relevant variables and rolls when entering final screen
                if currentScreen == 3:
                    creatureSpec = extractTable(screens[0].elements[1])
                    playersRoll = extractTable(screens[1].elements[1])
                    
                    for creature in creatureSpec:
                        if creatureSpec[creature][3] == '':
                            creatureSpec[creature][3] = 'opponent'
                            
                    creatureGroups, rolls = cc.rollCreatures(creatureSpec)
                    
                    screens[2].elements[2].contents = [[],[]]
                    for g, group in enumerate(creatureGroups):
                        screens[2].elements[2].contents[0].append(group)
                        screens[2].elements[2].contents[1].append(str(int(rolls[g])))
                        
                    #Adds players to the creatureGroup dictionary
                    for playerName in playersRoll:
                        player = cc.Creature('player', 'ally')
                        creatureGroups[playerName] = []
                        creatureGroups[playerName].append(player)
                        
                        #Adds player's rolls
                        rolls.append(playersRoll[playerName][0])
                    
                    rolls, closed = checkRepeats(creatureGroups, rolls, screens[2], display)
                    
            elif screens[nScreens-1].nextButton.active:
                screens[currentScreen-1].nextButton.active = False
                pg.quit
                return creatureGroups, rolls
                    
        
        allRolls.elements[1].getContents(playerRolls.elements[1])
        
        screens[currentScreen-1].draw(display)
        pg.display.update()
        clock.tick(tickRate)
    pg.quit()
    
def combatTracker(creatureGroups, rolls):
    
    initOrder = cc.initiativeOrder(creatureGroups, rolls)
    
    return