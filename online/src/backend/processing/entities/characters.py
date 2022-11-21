import random as rd

from . import objects as obj
from .static_functions import rollDamage
from . import attacks as at


class Character(obj.Entity):
    def __init__(self, entityName):
        super().__init__(entityName)
        self.baseEvasion = 0
        self.baseArmour = 0
        self.baseMovement = 0
        self.base_attacks = []

        self.hitProf = 0
        self.hands = 2
        
        self.baseStat = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'WIT': 0
            }
        self.stat = {}

        self.initiative = 0

        self.actionsTotal = 2
        self.reactionsTotal = 1

        self.actions = 2
        self.reactions = 1

        self.movement = 0

        self.evasion = {
            'Melee': {
                'piercing': 0,
                'slashing': 0,
                'bludgeoning': 0
            },
            'Ranged': 0
        }

        self.attack_options = []

        self.maxMovement = 0
        self.maxHealth = 0

        self.equippedWeapons = {
            'Left': None,
            'Right': None,
            'Both': None
        }

        self.equippedArmour = {
            'Light': None,
            'Heavy': None
        }

        self.inventory = []

        self.baseReach = 5

        self.reach = 0
        
        self.is_conscious = True
        self.is_stable = True
        self.savingThrows = (0, 0)
        self.drop_rate = 0

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
        self.reactions = self.reactionsTotal

    # Calculates the initiative roll
    def calcInitiative(self):
        init_roll = rd.randint(1, self.stat['DEX'])
        self.initiative = init_roll

    # Makes an attack roll returning whether it 0:miss, 1:hit, 2:critical hit
    def hitContest(self, attack, hitBonus, opponent):

        # Picks which opponent evasion to use
        if attack.from_weapon.is_ranged:
            opponentRoll = rd.randint(1, opponent.evasion['Ranged'])
        else:
            opponentRoll = rd.randint(1, opponent.evasion['Melee'][attack.damage_maintype])

        ownRoll = rd.randint(1, self.stat['DEX'])
        ownResult = ownRoll + hitBonus

        if ownResult > 10*opponentRoll:
            result = 2
        elif ownResult > opponentRoll:
            result = 1
        else:
            result = 0

        return result

    # Performs a single attack on another entity
    def singleAttack(self, attackID, creature):
        attack = self.attack_options[attackID]

        hitBonus = self.hitProf

        hitResult = self.hitContest(attack, hitBonus, creature)

        if attack.from_weapon.is_finesse:
            dmg_stat = max(self.stat['DEX'], self.stat['STR'])
        else:
            dmg_stat = self.stat['STR']

        if hitResult > 0:
            if hitResult == 1:
                is_critical = False
            else:
                is_critical = True
            damage = rollDamage(attack, dmg_stat)
            appliedDamage = 0
            for damage_type in damage:
                appliedDamage += creature.takeDamage(damage[damage_type], damage_type, attack.from_weapon.is_brutal, is_critical)

            indicator = str(appliedDamage)
        else:
            indicator = 'Miss'

        return indicator

    # Makes an attack against another entity with the given attacks
    def attack(self, attackIDList, creature):
        indicatorList = []

        for attackID in attackIDList:
            indicator = self.singleAttack(attackID, creature)
            indicatorList.append(indicator)

        return indicatorList

    # Damages the character
    def takeDamage(self, damage, dmg_type, heavy_hit=False, critical=False):
        appliedDamage = damage

        armour = 0
        if not critical:
            if dmg_type in self.armour:
                armour = self.armour[dmg_type]
        if heavy_hit:
            if dmg_type == 'piercing':
                armour *= 0.5
            elif dmg_type == 'slashing':
                appliedDamage *= 1.2

        armour = int(armour)
        appliedDamage -= armour

        if dmg_type in self.vulnerabilities:
            appliedDamage *= 2
        elif dmg_type in self.resistances:
            appliedDamage *= 0.5

        if appliedDamage > 0:
            self.health -= appliedDamage
            self.checkAlive()
            if heavy_hit and dmg_type == 'bludgeoning':
                self.actions -= 1
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
                self.is_stable = False
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
        
    def refreshMovement(self):
        self.movement = self.maxMovement

    # Recalculates the entity AC
    def refreshStatAfterArmour(self):

        for dmg_type in self.armour:
            self.armour[dmg_type] = self.baseArmour
        self.maxMovement = self.baseMovement

        for i, armour_type in enumerate(self.equippedArmour):
            eq_armour = self.equippedArmour[armour_type]
            if eq_armour is None:
                continue
            value = eq_armour.value
            if i == 0:
                self.stat['DEX'] *= eq_armour.flex
                self.armour['slashing'] += value
                self.armour['piercing'] += value
                self.armour['bludgeoning'] += value
            elif i == 1:
                self.stat['DEX'] *= eq_armour.flex
                self.maxMovement -= eq_armour.weight
                self.armour['slashing'] += value
                self.armour['piercing'] += 0.8*value
                self.armour['bludgeoning'] += 0.2*value

        self.armour['slashing'] = int(self.armour['slashing'])
        self.armour['piercing'] = int(self.armour['piercing'])
        self.armour['bludgeoning'] = int(self.armour['bludgeoning'])
        self.stat['DEX'] = int(self.stat['DEX'])

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
            self.health = 10
            self.is_stable = True
            output = 'Saved'
        if dies:
            self.is_alive = False
            output = 'Died'
            
        return output

    # Turns the weapon, armour and inventory strings into entities
    def getEquipment(self):
        for hand in self.equippedWeapons:
            if self.equippedWeapons[hand] is not None:
                self.equippedWeapons[hand] = obj.Weapon(self.equippedWeapons[hand])
        for armour_type in self.equippedArmour:
            if self.equippedArmour[armour_type] is not None:
                self.equippedArmour[armour_type] = obj.Armour(self.equippedArmour[armour_type])

        self.createInventory()

    # Converts the list of base attacks from strings to classes
    def convAttacks(self):
        new_list = []
        for i, attack_str in enumerate(self.base_attacks):
            attack = at.Attack(attack_str)
            attack.id = i
            new_list.append(attack)
        self.base_attacks = new_list

    # Gets what attacks are available and adds them to the options list - also ids them
    def getAttackOptions(self):
        i = 0
        self.attack_options = []
        for location in self.equippedWeapons:
            weapon = self.equippedWeapons[location]
            if weapon is None:
                continue
            for attack in weapon.attacks:
                self.attack_options.append(attack)
                attack.id = i
                i += 1

        if not self.attack_options:
            self.attack_options = self.base_attacks

    # Turns the inventory into class object
    def createInventory(self):
        new_list = []
        for item_str in self.inventory:
            item = obj.Weapon(item_str)  # Converts to weapon for now
            new_list.append(item)
        self.inventory = new_list


# A playable character
class Player(Character):
    names = ['Robert', 'Arthur', 'Grork', 'Fosdron', 'Thulgraena', 'Diffros', 'Ayda', 'Tezug', 'Dor\'goxun', 'Belba']

    class_weapons = {
        'Beserker': ['axes', 'bludgeons', 'slashes'],
        'Gladiator': ['pierces', 'mythical', 'throwables'],
        'Ranger': ['bows', 'double_edged_swords', 'special'],
        'Knight': ['hybrids', 'double_edged_swords', 'shields'],
        'Archer': ['bows', 'crossbows', 'throwables'],
        'Professor': ['staves', 'wands', 'mythical'],
        'Samurai': ['single_edged_swords', 'throwables', 'bows']
    }

    def __init__(self, playerLevel=1, playerClass=None, playerName=None):
        if playerName is None:
            playerName = rd.choice(Player.names)
        self.lvl = playerLevel
        self.type = playerClass = 'Beserker'
        self.healthDice = 0

        self.chosen_weapons = []

        self.behaviour_type = 1
        self.team = 1

        self.base_attacks = ['hit']

        super().__init__(playerName)

        self.getStats()

        self.resetStats()
        self.resetHealth()

        self.refreshStatAfterWeapon()
        self.refreshStatAfterArmour()

        self.calcInitiative()

        self.calcProfB()
        self.calcHealth()
    
    # Gets the player stats
    def getStats(self):
        obj.Entity.entityStats.getPlayerStats(self)
        self.getEquipment()
        self.convAttacks()
        self.getClass()
    
    # Recalculates the entity stats after a level up
    def levelUp(self):
        self.lvl += 1
        self.calcProfB()
        self.calcHealth()

    # Unequips a weapon if one present in given location
    def unequipWeapon(self, location):
        weapon = self.equippedWeapons[location]
        if weapon is not None:
            self.equippedWeapons[location] = None
            self.inventory.append(weapon)

    # Equips a weapon
    def equipWeapon(self, invIndex, location):
        weapon = self.inventory[invIndex]

        if not weapon.is_Weapon:
            return

        if weapon.is_twoHanded:
            self.equipDoubleWeapon(invIndex)
        else:
            self.equipSingleWeapon(invIndex, location)

    # Equips a one-handed weapon
    def equipSingleWeapon(self, invIndex, location):
        weapon = self.inventory[invIndex]

        self.unequipWeapon('Both')
        self.unequipWeapon(location)

        self.equippedWeapons[location] = weapon

        self.inventory.pop(invIndex)

    # Equips a two-handed weapon
    def equipDoubleWeapon(self, invIndex):
        weapon = self.inventory[invIndex]

        for location in self.equippedWeapons:
            self.unequipWeapon(location)

        self.equippedWeapons['Both'] = weapon

        self.inventory.pop(invIndex)

    # Unequip a set of armour
    def unequipArmour(self, armour_type):
        armour = self.equippedArmour[armour_type]
        if armour is not None:
            self.equippedArmour[armour_type] = None
            self.inventory.append(armour)

    # Equip a set of armour
    def equipArmour(self, invIndex):
        armour = self.inventory[invIndex]

        if not armour.is_Armour:
            return

        self.unequipArmour(armour.type)

        self.equippedArmour[armour.type] = armour

        self.inventory.pop(invIndex)

    # Calculates the entity proficiency bonus
    def calcProfB(self):
        self.hitProf = self.lvl * 5 + 5

    # Calculates health based on level and con mod
    def calcHealth(self):
        self.baseHealth = self.lvl * self.healthDice + self.stat['CON']
        self.maxHealth = self.baseHealth

    # Performs a single attack on another entity
    def singleAttack(self, attackID, creature):
        attack = self.attack_options[attackID]

        if attack.from_weapon.type in self.chosen_weapons:
            hitBonus = self.hitProf
        else:
            hitBonus = 0

        hitResult = self.hitContest(attack, hitBonus, creature)

        if attack.from_weapon.is_finesse:
            dmg_stat = max(self.stat['DEX'], self.stat['STR'])
        else:
            dmg_stat = self.stat['STR']

        if hitResult > 0:
            if hitResult == 1:
                is_critical = False
            else:
                is_critical = True
            damage = rollDamage(attack, dmg_stat)
            appliedDamage = 0
            for damage_type in damage:
                appliedDamage += creature.takeDamage(damage[damage_type], damage_type, attack.from_weapon.is_brutal, is_critical)

            indicator = str(appliedDamage)
        else:
            indicator = 'Miss'

        return indicator

    # Recalculates the entity damage and reach
    def refreshStatAfterWeapon(self):

        self.evasion['Melee']['piercing'] = self.baseEvasion
        self.evasion['Melee']['slashing'] = self.baseEvasion
        self.evasion['Melee']['bludgeoning'] = self.baseEvasion
        self.evasion['Ranged'] = self.baseEvasion
        self.reach = self.baseReach
        self.getAttackOptions()

        for hand in self.equippedWeapons:
            eq_weapon = self.equippedWeapons[hand]
            if eq_weapon is None:
                continue
            if not eq_weapon.is_ranged:
                if eq_weapon.range > self.reach:
                    self.reach = eq_weapon.range
            if eq_weapon.defense_type:
                protection = eq_weapon.protection
                if eq_weapon.type in self.chosen_weapons:
                    protection *= 2
                self.evasion['Melee']['piercing'] += protection
                self.evasion['Melee']['slashing'] += protection
                self.evasion['Melee']['bludgeoning'] += protection
                if eq_weapon.defense_type == 'shield':
                    self.evasion['Ranged'] += protection
                    self.evasion['Melee']['bludgeoning'] -= protection
                    self.armour['bludgeoning'] += int(protection / 2)

    # Gets the trait associated with the player's class
    def getClass(self):
        self.chosen_weapons = Player.class_weapons[self.type]


# A non-playable character
class NPC(Character):
    def __init__(self, npcName):
        self.target = None
        self.behaviour_type = 2
        self.team = 1
        self.hitProf = 0

        self.starting_items = []

        super().__init__(npcName)

        self.getStats()

        self.resetStats()
        self.resetHealth()

        self.refreshStatAfterWeapon()
        self.refreshStatAfterArmour()

        self.calcInitiative()

    # Collects entity base stats
    def getStats(self):
        obj.Entity.entityStats.getCharacterStats(self)
        self.getEquipment()
        self.convAttacks()

    # Recalculates the entity damage and reach
    def refreshStatAfterWeapon(self):

        self.evasion['Melee']['piercing'] = self.baseEvasion
        self.evasion['Melee']['slashing'] = self.baseEvasion
        self.evasion['Melee']['bludgeoning'] = self.baseEvasion
        self.evasion['Ranged'] = self.baseEvasion
        self.reach = self.baseReach
        self.getAttackOptions()

        for hand in self.equippedWeapons:
            eq_weapon = self.equippedWeapons[hand]
            if eq_weapon is None:
                continue
            if not eq_weapon.is_ranged:
                if eq_weapon.range > self.reach:
                    self.reach = eq_weapon.range
            if eq_weapon.defense_type:
                protection = eq_weapon.protection
                if eq_weapon.name in self.starting_items:
                    protection *= 2
                self.evasion['Melee']['piercing'] += protection
                self.evasion['Melee']['slashing'] += protection
                self.evasion['Melee']['bludgeoning'] += protection
                if eq_weapon.defense_type == 'shield':
                    self.evasion['Ranged'] += protection
                    self.evasion['Melee']['bludgeoning'] -= protection
                    self.armour['bludgeoning'] += int(protection / 2)


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
