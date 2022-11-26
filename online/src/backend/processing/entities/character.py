import random as rd

from . import entity as ent
from . import attack as at
from . import item as it


class Character(ent.HealthEntity):
    def __init__(self, entityName):
        super().__init__(entityName)
        self.baseEvasion = 0
        self.baseArmour = 0
        self.baseMovement = 0
        self.baseCoverage = 0
        self.base_attacks = []

        self.dmg_mult = 1  # For larger creatures to do more damage

        self.hitProf = 0
        
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
            'Under': None,
            'Over': None
        }
        self.coverage = 0

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

    # Resets health to max health
    def refreshHealth(self):
        self.health = self.maxHealth
    
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

        crit_weighting = opponent.stat['DEX'] * opponent.coverage + (20 - opponent.size)

        if attack.type == 'bludgeoning':
            crit_weighting = int(0.5 * crit_weighting)

        # Picks which opponent evasion to use
        if not attack.from_weapon.is_ranged and attack.damage_maintype in opponent.evasion['Melee']:
            opponentRoll = rd.randint(1, opponent.evasion['Melee'][attack.damage_maintype])
        else:
            opponentRoll = rd.randint(1, opponent.evasion['Ranged'])

        ownRoll = rd.randint(1, self.stat['DEX'])
        ownResult = ownRoll + hitBonus

        if ownResult > crit_weighting*opponentRoll:
            result = 2
        elif ownResult > opponentRoll:
            result = 1
        else:
            result = 0

        return result

    # Performs a single attack on another entity
    def singleAttack(self, attackID, creature):
        attack = self.attack_options[attackID]

        if attack.from_weapon is None:
            hitBonus = self.hitProf
        elif self.is_Proficient(attack.from_weapon):
            hitBonus = self.hitProf
        else:
            hitBonus = 0

        hitResult = self.hitContest(attack, hitBonus, creature)

        dmg_stat = self.stat['STR']
        if attack.from_weapon is not None:
            if attack.from_weapon.is_finesse:
                dmg_stat *= 1 + self.stat['DEX'] / 100

        if hitResult > 0:
            if hitResult == 1:
                is_critical = False
            else:
                is_critical = True
            damage = attack.rollDamage(dmg_stat)
            appliedDamage = 0
            is_AP = attack.from_weapon.is_AP
            if creature.equippedArmour['Over'] is not None:
                if creature.equippedArmour['Over'].material == 'mail' and attack.from_weapon.is_fine:
                    is_AP = True
            for damage_type in damage:
                appliedDamage += creature.takeDamage(damage[damage_type], damage_type, is_AP, is_critical)

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
                if self.is_Proficient(eq_weapon):
                    protection *= 2
                self.evasion['Melee']['piercing'] += protection
                self.evasion['Melee']['slashing'] += protection
                self.evasion['Melee']['bludgeoning'] += protection
                if eq_weapon.defense_type == 'shield':
                    self.evasion['Ranged'] += protection
                    self.evasion['Melee']['bludgeoning'] -= protection

    # Recalculates the entity AC
    def refreshStatAfterArmour(self):

        for dmg_type in self.armour:
            self.armour[dmg_type] = self.baseArmour
        self.maxMovement = self.baseMovement
        self.coverage = self.baseCoverage

        for armour_type in self.equippedArmour:
            eq_armour = self.equippedArmour[armour_type]
            if eq_armour is None:
                continue
            material = eq_armour.material
            value = eq_armour.value
            self.stat['DEX'] *= eq_armour.flex
            self.maxMovement -= eq_armour.weight
            self.coverage += eq_armour.coverage / 100
            if material == 'cloth':
                self.armour['slashing'] += value
                self.armour['piercing'] += 0.5 * value
                self.armour['bludgeoning'] += value
            elif material == 'mail':
                self.armour['slashing'] += value
                self.armour['piercing'] += 0.5 * value
            elif material == 'plate':
                self.armour['slashing'] += value
                self.armour['piercing'] += value
                self.armour['bludgeoning'] += 0.5 * value

        if self.coverage > 1:
            self.coverage = 1

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
                self.equippedWeapons[hand] = it.Weapon(self.equippedWeapons[hand])
        for armour_type in self.equippedArmour:
            if self.equippedArmour[armour_type] is not None:
                self.equippedArmour[armour_type] = it.Armour(self.equippedArmour[armour_type])

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
            item = it.Weapon(item_str)  # Converts to weapon for now
            new_list.append(item)
        self.inventory = new_list

    # Functions to be redefined with npc and player classes
    def is_Proficient(self, weapon):
        pass
