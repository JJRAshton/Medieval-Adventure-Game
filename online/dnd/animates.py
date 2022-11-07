from objects import Entity

class AnimateEntity(Entity):
    def __init__(self):
        super().__init__(self)
        self.lvl = 0
        self.maxMovement = 0
        self.type = None
        
        self.baseStat = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'INT': 0,
            'WIS': 0,
            'CHAR': 0
            }
        
        self.actions = []
        self.actionsTotal = 1
        self.attacksTotal = 1
        self.actions = 1
        self.attacks = 1
        
        self.hitDiceValue = 0
        self.hitDiceNumber = 0
        
        self.primaryWeapon = None
        self.armour = None
        
        self.movement = 0
        
        self.unconscious = False
        self.savingThrows = (0,0)
        
        self.resetStats()
        self.levelUp()
        self.refreshModifierStat()
        self.refreshArmourStat()
        self.refreshWeaponStat()
    
    #Moves entity by given vector and decreases movement
    def move(self, vector):
        super().move(vector)
        count = abs(vector[0])+abs(vector[1])
        self.movement -= 5*count
        
    #Checks if player is still alive
    def checkHealth(self):
        if self.health < 0:
            if abs(self.health) < self.baseHealth:
                self.alive = False
            else:
                self.unconscious = True
            self.health = 0
            
    #Heals the entity
    def heal(self, damage):
        (number,dice,bonus) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1,dice)
        appliedHealing = base + bonus
        self.health += appliedHealing
            
    #Resets the stats to the base stats
    def resetStats(self):
        self.stat = {}
        for stat in self.baseStat:
            self.stat[stat] = self.baseStat[stat]
        
    def resetMovement(self):
        self.movement = self.maxMovement
        
    #Recalculates the entity stats after a change of stats
    def refreshModifierStat(self):
        self.mod = {}
        for stat in self.stat:
            self.mod[stat] = int((self.stat[stat]-self.stat[stat]%2)/2)-5
    
    #Recalculates the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.baseHealth = self.con+self.hitDiceValue + (self.lvl-1)*(self.mod['CON']+0.5+self.hitDiceValue/2)
    
    #Recalculates the entity AC
    def refreshArmourStat(self):
        if self.armour.type == 'Heavy':
            self.AC = self.armour.armourValue
        elif self.armour.type == 'Medium':
            self.AC = self.armour.armourValue + min(self.mod['DEX'],2)
        elif self.armour.type == 'Light':
            self.AC = self.armour.armourValue + self.mod['DEX']
        elif self.armour == None:
            self.AC = self.mod['DEX']
        
    #Recalculates the entity damage and reach
    def refreshWeaponStat(self):
        self.reach = self.primaryWeapon.reach
        if self.primaryWeapon.finesse:
            self.damage = (self.primaryWeapon.damage[0], self.primaryWeapon.damage[1], max(self.mod['STR'],self.mod['DEX']))
        else:
            self.damage = (self.primaryWeapon.damage[0], self.primaryWeapon.damage[1], self.mod['STR'])
        
    #Makes a saving throw
    def makeSavingThrow(self):
        throw = rd.randint(1,20)
        saved = False
        dies = False
        
        if throw == 1:
            self.savingThrows = (self.savingThrows[0],self.savingThrows[1]+2)
            output = 'Critical Fail'
        elif throw < 10:
            self.savingThrows = (self.savingThrows[0],self.savingThrows[1]+1)
            output = 'Fail'
        elif throw == 20:
            saved = True
            output = 'Critical Success!'
        else:
            self.savingThrows = (self.savingThrows[0]+1,self.savingThrows[1])
            output = 'Success!'
            
        if self.savingThrows[0] >= 3:
            saved = True
        elif self.savingThrow[1] >= 3:
            dies = True
            
        if saved:
            self.health = 1
            self.stable = True
            output = 'Saved'
        if dies:
            self.dead = True
            output = 'Died'
            
        return output
    
    #Collects entity end stats
    def overrideStats(self): # temporary measure to work with just these stats
        self.baseSize = 
        self.health = 
        self.AC = 
        self.primaryWeapon = 
        self.mod['STR'] = 
        self.profBonus = 
        self.maxMovement = 
        
    #Collects entity base stats
    def getStats(self): # yet to get from jamie
        super().getStats(self)
        self.lvl
        self.maxMovement
        self.type
        
        self.armour
        self.primaryWeapon
        
#A playable character        
class Player(AnimateEntity):
    def __init__(self):
        super().__init__(self)

#A non-playable character        
class NPC(AnimateEntity):
    def __init__(self):
        super().__init__(self)
        self.target = None

#A hostile character        
class Monster(NPC):
    def __init__(self):
        super().__init__(self)
        
    #Checks if entity is still alive
    def checkHealth(self):
        if self.health < 0:
            self.alive = False
            self.health = 0