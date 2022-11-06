
class Entity:
    def __init__(self):
        self.lvl = 0
        self.movement = 0
        
        self.strStat = 0
        self.dexStat = 0
        self.conStat = 0
        self.intStat = 0
        self.wisStat = 0
        self.charStat = 0
        
        self.weapon = None
        self.armour = None
        
        self.size = 'Medium'
        
        self.inventory = []
        
        self.health = 0
        
        self.refreshModifierStat()
        self.refreshArmourStat()
        self.refreshWeaponStat()
    
    #Collects entity stats
    def getStats(self):
        
        
    #Recalculates the creature stats after a change of stats
    def refreshModifierStat(self):
        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.char = 0
    
    #Recalculates the creature stats after change of armour
    def refreshArmourStat(self):
        if self.armour.type == 'Heavy':
            self.AC = self.armour.armour
        elif self.armour.type == 'Medium':
            self.AC = self.armour.armour + min(self.dex,2)
        elif self.armour.type == 'Light':
            self.AC = self.armour.armour + self.dex
        elif self.armour == None:
            self.AC = self.dex
        
    #Recalculates the creature stats after change of weapon
    def refreshWeaponStat(self):
        self.damage = self.weapon.damage
        self.reach = self.weapon.reach
        
class Object:
    def __init__(self):
        self.size = 0
        self.weight = 0
        
class Weapon(Object):
    def __init__(self):
        Object.__init__(self)
        self.damage = 0
        self.reach = 5
        
        self.loading = False
        self.ammunition = False
        self.light = False
        self.heavy = False
        
class Armour(Object):
    def __init__(self):
        Object.__init__(self)
        self.type = ''
        self.armour = 0
        
class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        
class Creature(Entity):
    def __init__(self):
        Entity.__init__(self)
        
class Monster(Creature):
    def __init__(self):
        Creature.__init__(self)