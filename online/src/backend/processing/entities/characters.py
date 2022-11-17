import random as rd

from . import objects as obj


class Character(obj.Entity):
    def __init__(self, entityName):
        super().__init__(entityName)
        self.baseEvasion = 0
        self.baseArmour = 0
        self.baseMovement = 0

        self.hitProf = 0
        self.hands = 2
        
        self.baseStat = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'WIT': 0
            }
        self.stat = {}
        self.mod = {}

        self.initiative = 0

        self.actionsTotal = 2
        self.attacksTotal = 1
        self.reactionsTotal = 1

        self.actions = 2
        self.attacks = 1
        self.reactions = 1

        self.movement = 0
        
        self.hitDiceValue = 0
        self.hitDiceNumber = 0

        self.maxMovement = 0
        self.maxHealth = 0

        self.equippedWeapons = {
            'Left': None,
            'Right': None
        }

        self.equippedArmour = {
            'Light': None,
            'Medium': None,
            'Heavy': None
        }

        self.inventory = []

        self.baseReach = 5

        self.dmgMod = {
            'Left': 0,
            'Right': 0
        }
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

    # Initialises the relevant stats to start a new turn
    def initialiseTurn(self):
        self.movement = self.maxMovement

        self.actions = self.actionsTotal
        self.attacks = self.attacksTotal
        self.reactions = self.reactionsTotal

    # Calculates the initiative roll
    def calcInitiative(self):
        init_roll = rd.randint(1, 20)
        self.initiative = init_roll + self.mod['DEX']

    # Makes an attack roll returning whether it 0:miss, 1:hit, 2:critical hit
    def hitRoll(self, hitBonus, opponent_evasion):

        roll = rd.randint(1, 20)
        if roll == 20:
            result = 2
        elif roll + hitBonus < opponent_evasion:
            result = 0
        else:
            result = 1

        return result

    # Performs a single attack on another entity
    def singleAttack(self, hand, creature):
        weapon = self.equippedWeapons[hand]

        if weapon is None:
            damage = (self.mod['STR'], 4)
            dmg_type = 'bludgeon'
        else:
            damage = weapon.damage
            dmg_type = weapon.dmg_type
        dmgMod = self.dmgMod[hand]

        hitBonus = self.mod['DEX'] + self.hitProf

        rollResult = self.hitRoll(hitBonus, creature.evasion)

        if rollResult > 0:
            if rollResult == 1:
                appliedDamage = creature.takeDamage(damage, dmgMod, dmg_type)
            else:   # critical
                appliedDamage = creature.takeDamage(damage, dmgMod, dmg_type, True)
            indicator = str(appliedDamage)
        else:
            indicator = 'Miss'

        return indicator

    # Makes an attack against another entity
    def attack(self, creature):
        if self.equippedWeapons['Left'] is not None and self.equippedWeapons['Right'] is not None:
            if self.equippedWeapons['Left'].is_light and self.equippedWeapons['Right'].is_light:
                self.singleAttack('Left', creature)
                self.singleAttack('Right', creature)
            elif self.equippedWeapons['Left'].is_twoHanded:
                self.singleAttack('Left', creature)
            elif self.equippedWeapons['Left'].avdmg > self.equippedWeapons['Right'].avdmg:
                self.singleAttack('Left', creature)
            else:
                self.singleAttack('Right', creature)
        elif self.equippedWeapons['Left'] is None and self.equippedWeapons['Right'] is None:
            self.singleAttack('Right', creature)
        elif self.equippedWeapons['Left'] is None:
            self.singleAttack('Right', creature)
        else:
            self.singleAttack('Left', creature)

    # Damages the character
    def takeDamage(self, damage, bonus, dmg_type, heavy_hit=False, critical=False):
        (number, dice) = damage
        base = 0
        for _ in range(number):
            base += rd.randint(1, dice)

        if dmg_type in self.vulnerabilities:
            appliedDamage = 2 * (base + bonus)
        elif dmg_type in self.resistances:
            appliedDamage = int(0.5 * (base + bonus))
        else:
            appliedDamage = base + bonus

        armour = 0
        if not critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
        if heavy_hit:
            if dmg_type == 'pierce':
                armour *= 0.5
            elif dmg_type == 'slash':
                appliedDamage *= 1.2
            elif dmg_type == 'bludgeon':
                self.actions -= 1

        appliedDamage -= armour

        if appliedDamage > 0:
            self.health -= appliedDamage
            self.checkAlive()
        else:
            appliedDamage = 0

        return appliedDamage

    # Makes an opportunity attack
    def oppAttack(self, creature):
        pass

    # Checks if entity is still alive
    def checkAlive(self):
        if self.health <= 0:
            if abs(self.health) < self.baseHealth:
                self.is_alive = False
            else:
                self.is_conscious = False
            self.health = 0
            
    # Heals the entity
    def heal(self, appliedHealing):
        self.health += appliedHealing
        if self.health > self.maxHealth:
            self.health = self.maxHealth
            
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
        for dmg_type in self.armour:
            self.armour[dmg_type] = self.baseArmour
        self.maxMovement = self.baseMovement
        self.evasion = self.baseEvasion

        for i, armour_type in enumerate(self.equippedArmour):
            eq_armour = self.equippedArmour[armour_type]
            if eq_armour is None:
                continue
            if i == 0:
                self.evasion -= 1
                for dmg_type in self.armour:
                    self.armour[dmg_type] += eq_armour.value
            elif i == 1:
                self.evasion -= 3
                self.armour['slash'] += eq_armour.value
                self.armour['pierce'] += 0.3*eq_armour.value
                self.armour['bludgeon'] += 0.1*eq_armour.value
            elif i == 2:
                self.evasion -= 6
                self.maxMovement -= 10
                self.armour['slash'] += eq_armour.value
                self.armour['pierce'] += 0.9*eq_armour.value
                self.armour['bludgeon'] += 0.15*eq_armour.value
        
    # Recalculates the entity damage and reach
    def refreshWeaponStat(self):
        self.reach = self.baseReach
        for hand in self.equippedWeapons:
            eq_weapon = self.equippedWeapons[hand]
            if eq_weapon is None:
                self.dmgMod[hand] = self.mod['STR']
                continue
            if eq_weapon.reach > self.reach:
                self.reach = eq_weapon.reach
            if eq_weapon.is_finesse:
                self.dmgMod[hand] = max(self.mod['STR'], self.mod['DEX'])
            else:
                self.dmgMod[hand] = self.mod['STR']

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
        self.getEquipment()

    # Turns the weapon and armour strings into entities
    def getEquipment(self):
        for hand in self.equippedWeapons:
            if self.equippedWeapons[hand] is not None:
                self.equippedWeapons[hand] = obj.Weapon(self.equippedWeapons[hand])
        for armour_type in self.equippedArmour:
            if self.equippedArmour[armour_type] is not None:
                self.equippedArmour[armour_type] = obj.Armour(self.equippedArmour[armour_type])


# A playable character
class Player(Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']

    class_weapons = {
        'Beserker': ['axes', 'bludgeons', 'slashes'],
        'Gladiator': ['pierces', 'mythical', 'throwables'],
        'Ranger': ['bows', 'double_edged_swords', 'special'],
        'Knight': ['hybrids', 'double_edged_swords', 'pierces'],
        'Archer': ['bows', 'crossbows', 'throwables'],
        'Professor': ['staves', 'wands', 'mythical'],
        'Samurai': ['single_edged_swords', 'throwables', 'bows']
    }

    def __init__(self, playerLevel=1, playerClass=None, playerName=None):
        if playerName is None:
            playerName = rd.choice(Player.names)
        self.lvl = playerLevel
        self.type = playerClass = 'Beserker'
        super().__init__(playerName)

        self.chosen_weapons = []

        self.behaviour_type = 1
        self.team = 1

        self.calcProfB()
        self.calcHealth()
    
    # Gets the player stats
    def getStats(self):
        obj.Entity.entityStats.getPlayerStats(self)
        self.getEquipment()
    
    # Recalculates the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.calcProfB()
        self.calcHealth()

    # Calculates the entity proficiency bonus
    def calcProfB(self):
        # self.profBonus = int(((self.lvl - 1) - (self.lvl - 1) % 4) / 4) + 2
        self.hitProf = self.lvl + 2

    # Calculates health based on level and con mod
    def calcHealth(self):
        self.baseHealth = self.mod['CON']+self.hitDiceValue + (self.lvl-1)*(self.mod['CON']+0.5+self.hitDiceValue/2)
        self.maxHealth = self.baseHealth

    # Performs a single attack on another entity
    def singleAttack(self, hand, creature):
        weapon = self.equippedWeapons[hand]

        if weapon is None:
            damage = (self.mod['STR'], 4)
            dmg_type = 'bludgeon'
        else:
            damage = weapon.damage
            dmg_type = weapon.dmg_type
        dmgMod = self.dmgMod[hand]

        hitBonus = self.mod['DEX']
        if weapon.type in self.chosen_weapons:
            hitBonus += self.hitProf

        rollResult = self.hitRoll(hitBonus, creature.evasion)

        if rollResult > 0:
            if rollResult == 1:
                appliedDamage = creature.takeDamage(damage, dmgMod, dmg_type)
            else:  # critical
                appliedDamage = creature.takeDamage(damage, dmgMod, dmg_type, True)
            indicator = str(appliedDamage)
        else:
            indicator = 'Miss'

        return indicator

    # Gets the trait associated with the player's class
    def getClass(self):
        self.chosen_weapons = Player.class_weapons[self.type]


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
    def checkAlive(self):
        if self.health < 0:
            self.is_alive = False
            self.health = 0
