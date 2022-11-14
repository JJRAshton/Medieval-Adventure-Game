import random as rd

from . import objects as obj


class Character(obj.Entity):
    def __init__(self, entityName):
        super().__init__(entityName)
        self.maxMovement = 0
        self.profBonus = 0
        
        self.baseStat = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'INT': 0,
            'WIS': 0,
            'CHAR': 0
            }
        self.stat = {}
        self.mod = {}

        self.initiative = 0

        self.actionsTotal = 1
        self.attacksTotal = 1
        self.reactionsTotal = 1
        self.bonusactionsTotal = 0

        self.actions = 1
        self.attacks = 1
        self.reactions = 1
        self.bonusactions = 0

        self.movement = 0
        
        self.hitDiceValue = 0
        self.hitDiceNumber = 0
        
        self.baseArmour = 10

        self.primaryWeapon = None
        self.armour = None

        self.inventory = []

        self.baseDamage = (0, 0)

        self.damage = (0, 0, 0)
        self.atkMod = 0
        self.reach = 0
        
        self.is_conscious = True
        self.is_stable = False
        self.savingThrows = (0, 0)
        self.drop_rate = 0
        
        self.getStats()

        self.resetStats()
        self.resetHealth()

        self.refreshModifierStat()
        self.refreshArmourStat()
        self.refreshWeaponStat()

        self.calcInitiative()

    # Allows for sorting by initiative order in sorted list
    def __lt__(self, other):
        return self.initiative > other.initiative
    
    # Moves entity by given vector and decreases movement
    def move(self, vector):
        super().move(vector)
        count = abs(vector[0])+abs(vector[1])
        self.movement -= 5*count

        # Moves characters held items
        for item in self.inventory:
            item.move(vector)
        if self.primaryWeapon is not None:
            self.primaryWeapon.move(vector)
        if self.armour is not None:
            self.armour.move(vector)

    # Initialises the relevant stats to start a new turn
    def initialiseTurn(self):
        self.movement = self.maxMovement

        self.actions = self.actionsTotal
        self.attacks = self.attacksTotal
        self.reactions = self.reactionsTotal
        self.bonusactions = self.bonusactionsTotal

    # Calculates the initiative roll
    def calcInitiative(self):
        init_roll = rd.randint(1,20)
        self.initiative = init_roll + self.mod['DEX']
    
    # Makes an attack roll returning whether it 0:critical fail, 1:miss, 2:hit, 3:critical hit
    def attackRoll(self, armourClass):
        atkBonus = self.atkMod + self.profBonus
        roll = rd.randint(1, 20)

        if roll == 1:
            result = 0
        elif roll == 20:
            result = 3
        elif roll+atkBonus < armourClass:
            result = 1
        else:
            result = 2

        return result

    # Performs an attack on another entity
    def attack(self, creature):
        rollResult = self.attackRoll(creature.armourClass)

        if rollResult > 1:
            if rollResult == 2:
                damage = self.damage
            else:   # roll result = 3
                damage = (2*self.damage[0], self.damage[1], self.damage[2])
            appliedDamage = creature.takeDamage(damage)
            indicator = str(appliedDamage)
        else:
            indicator = 'Whiff'

        return indicator

    # Makes an opportunity attack
    def oppAttack(self, creature):
        self.attack(creature)
        self.reactions -= 1

    # Checks if entity is still alive
    def checkHealth(self):
        if self.health <= 0:
            if abs(self.health) < self.baseHealth:
                self.is_alive = False
            else:
                self.is_conscious = False
            self.health = 0
            
    # Heals the entity
    def heal(self, damage):
        (number, dice, bonus) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1, dice)
        appliedHealing = base + bonus
        self.health += appliedHealing
            
    # Resets the stats to the base stats
    def resetStats(self):
        for stat in self.baseStat:
            self.stat[stat] = self.baseStat[stat]
        
    def resetMovement(self):
        self.movement = self.maxMovement
        
    # Recalculates the entity modifiers after a change of stats
    def refreshModifierStat(self):
        for stat in self.stat:
            self.mod[stat] = int((self.stat[stat]-self.stat[stat] % 2)/2)-5

    # Recalculates the entity AC
    def refreshArmourStat(self):
        if self.armour.type == 'heavy':
            self.armourClass = self.armour.armourValue
        elif self.armour.type == 'medium':
            self.armourClass = self.armour.armourValue + min(self.mod['DEX'], 2)
        elif self.armour.type == 'light':
            self.armourClass = self.armour.armourValue + self.mod['DEX']
        elif self.armour is None:
            self.armourClass = self.baseArmour + self.mod['DEX']
        
    # Recalculates the entity damage and reach
    def refreshWeaponStat(self):
        if self.primaryWeapon is not None:
            self.reach = self.primaryWeapon.reach
            if self.primaryWeapon.is_finesse:
                self.atkMod = max(self.mod['STR'], self.mod['DEX'])
            else:
                self.atkMod = self.mod['STR']
            self.damage = (self.primaryWeapon.damage[0], self.primaryWeapon.damage[1], self.atkMod)
        else:
            self.reach = 5
            self.atkMod = self.mod['STR']
            self.damage = (self.baseDamage[0], self.baseDamage[1], self.atkMod)

    # Makes a saving throw
    def makeSavingThrow(self):
        throw = rd.randint(1, 20)
        saved = False
        dies = False
        
        if throw == 1:
            self.savingThrows = (self.savingThrows[0], self.savingThrows[1]+2)
            output = 'Critical Fail'
        elif throw < 10:
            self.savingThrows = (self.savingThrows[0], self.savingThrows[1]+1)
            output = 'Fail'
        elif throw == 20:
            saved = True
            output = 'Critical Success!'
        else:
            self.savingThrows = (self.savingThrows[0]+1, self.savingThrows[1])
            output = 'Success!'
            
        if self.savingThrows[0] >= 3:
            saved = True
        elif self.savingThrows[1] >= 3:
            dies = True
            
        if saved:
            self.health = 1
            self.is_stable = True
            output = 'Saved'
        if dies:
            self.is_alive = False
            output = 'Died'
            
        return output
        
    # Collects entity base stats
    def getStats(self):  # yet to get from jamie
        obj.Entity.entityStats.getCharacterStats(self)
        if self.primaryWeapon is not None and self.primaryWeapon != '':
            self.primaryWeapon = obj.Weapon(self.primaryWeapon)
        if self.armour is not None and self.armour != '':
            self.armour = obj.Armour(self.armour)


# A playable character
class Player(Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']
    
    def __init__(self, playerLevel=1, playerClass=None, playerName=None):
        if playerName is None:
            playerName = rd.choice(Player.names)
        super().__init__(playerName)
        self.lvl = playerLevel
        self.type = playerClass

        self.behaviour_type = 1
        self.team = 1

        self.calcProfB()
        self.calcHealth()
    
    # Gets the player stats
    def getStats(self):
        obj.Entity.entityStats.getPlayerStats(self)
        if self.primaryWeapon is not None and self.primaryWeapon != '':
            self.primaryWeapon = obj.Weapon(self.primaryWeapon)
        if self.armour is not None and self.armour != '':
            self.armour = obj.Armour(self.armour)
    
    # Recalculates the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.calcProfB()
        self.calcHealth()

    # Calculates the entity proficiency bonus
    def calcProfB(self):
        self.profBonus = int(((self.lvl - 1) - (self.lvl - 1) % 4) / 4) + 2

    # Calculates health based on level and con mod
    def calcHealth(self):
        self.baseHealth = self.mod['CON']+self.hitDiceValue + (self.lvl-1)*(self.mod['CON']+0.5+self.hitDiceValue/2)


# A non-playable character
class NPC(Character):
    def __init__(self, npcName):
        super().__init__(npcName)
        self.target = None
        self.behaviour_type = 2
        self.team = 1


# A hostile character
class Monster(NPC):
    def __init__(self, monsterName):
        super().__init__(monsterName)
        self.team = 2
        
    # Checks if entity is still alive
    def checkHealth(self):
        if self.health < 0:
            self.is_alive = False
            self.health = 0
