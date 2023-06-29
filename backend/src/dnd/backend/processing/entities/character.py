import random as rd
from typing import Dict, List, Tuple

from .stats.make_dataframes import AttackStatDictionaryProvider
from . import entity as ent
from .health_entity import HealthEntity
from .stats.attack_factory import AttackFactory
from .stats.weapon_factory import WeaponFactory
from .attack import Attack
from . import item as it


# Gets the in game distance between two coords for attacks
def calc_rad_dist(coords1: Tuple[int, int], coords2: Tuple[int, int]):
    xdiff = abs(coords2[0] - coords1[0])
    ydiff = abs(coords2[1] - coords1[1])

    maxdiff = max(xdiff, ydiff)
    dist = 5 * maxdiff

    return dist


class Character(HealthEntity):
    def __init__(self, entityName: str):
        super().__init__(entityName)
        stat_provider = AttackStatDictionaryProvider()
        self.__attack_factory = AttackFactory(stat_provider)
        self.__weapon_factory = WeaponFactory(stat_provider,  self.__attack_factory)
        self.base_evasion = 0
        self.base_armour = 0
        self.base_movement = 0
        self.base_coverage = 0
        self.base_attacks: List[Attack] = []

        self.dmg_mult = 1  # For larger creatures to do more damage

        self.skill = 0
        
        self.base_stat = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'WIT': 0
            }
        self.stat: Dict[str, int] = {}

        self.initiative = 0

        self.actions_total = 2
        self.reactions_total = 1

        self.actions = 2
        self.reactions = 1

        self.movement = 0

        self.evasion = {
            'Melee': 0,
            'Ranged': 0
        }

        self.attack_options = []

        self.max_movement = 0
        self.max_health = 0

        self.equipped_weapons: Dict[str, str | None] = {
            'Left': None,
            'Right': None,
            'Both': None
        }

        self.equipped_armour = {
            'Under': None,
            'Over': None
        }
        self.coverage = 0
        self.bulk = 0

        self.inventory = []

        self.base_reach: int = 5

        self.reach: int = 0
        self.range: int = 0
        
        self.is_conscious: bool = True
        self.is_stable: bool = True
        self.saving_throws = (0, 0)
        self.drop_rate: float = 0

    # Allows for sorting by initiative order in sorted list
    def __lt__(self, other) -> bool:
        return self.initiative > other.initiative

    # Resets health to max health
    def refreshHealth(self):
        self.health = self.max_health
    
    # Moves entity by given vector and decreases movement
    def move(self, vector: Tuple[int, int]):
        super().move(vector)
        count = abs(vector[0])+abs(vector[1])
        self.movement -= 5*count

    # Initialises the relevant stats to start a new turn
    def initialiseTurn(self):
        self.movement = self.max_movement

        self.actions = self.actions_total
        self.reactions = self.reactions_total

    # Calculates the initiative roll
    def calcInitiative(self):
        if self.stat['DEX'] > 1:
            init_roll = rd.randint(1, self.stat['DEX'])
        else:
            init_roll = 1
        self.initiative = init_roll

    # To be used in player for finding class traits
    def has_Trait(self, trait_str: str):
        return False

    # Makes a stat roll with given stat depending on condition -1: disadv, 0: normal, 1: adv
    def statRoll(self, stat: str, condition: int=0):
        if stat not in self.stat:
            raise ValueError

        if condition == -1:  # Disadvantage
            return rd.randint(1, int(self.stat[stat]**0.5))
        elif condition == 1:  # Advantage
            return rd.randint(1, self.stat[stat]**2)
        elif condition == 0:  # Normal
            return rd.randint(1, self.stat[stat])

        else:
            raise ValueError

    # Makes an attack roll returning whether it -1:miss, 0:blocked, 1:hit, 2:critical hit
    def hitContest(self, attack: Attack, hitBonus, opponent):

        distance = calc_rad_dist(self.coords, opponent.coords)
        size_diff = self.size - opponent.size

        opponentCritResistance = opponent.stat['DEX'] * ((1 + opponent.coverage) ** 2)

        if 'bludgeoning' == attack.damage_maintype:
            crit_weighting = opponentCritResistance
        else:
            crit_weighting = opponentCritResistance + size_diff

        if self.has_Trait('Keen_eye'):  # Increased crit chance
            crit_weighting = int(crit_weighting * (1 - self.stat['WIT'] / 100))

        if crit_weighting < 0:
            crit_weighting = 0

        # Picks which opponent evasion to use
        if attack.from_weapon.is_melee:
            opponentEvasion = opponent.evasion['Melee']
        else:
            opponentEvasion = opponent.evasion['Ranged']

        if opponentEvasion <= 1:
            opponentRoll = 1
        else:
            opponentRoll = rd.randint(1, opponentEvasion)

        if attack.from_weapon.is_ranged and distance == 5:
            ownRoll = self.statRoll('DEX', -1)  # Disadvantage at close range for ranged weapons
        else:
            ownRoll = self.statRoll('DEX')

        ownResult = ownRoll + hitBonus

        if ownResult >= crit_weighting*opponentRoll:
            result = 2
        elif ownResult > opponentRoll:
            result = 1
        elif ownResult > opponentRoll - (opponentEvasion - opponent.baseEvasion):
            result = 0
        else:
            result = -1

        return result

    # Performs a single attack on another entity
    def singleAttack(self, attackID: int, creature: HealthEntity):
        attack: Attack = self.attack_options[attackID]

        AA_stat = self.stat['WIT'] if self.has_Trait('Anti-armour_expert') else None

        if attack.from_weapon is None:
            hitBonus = self.skill
        elif self.is_Proficient(attack.from_weapon):
            hitBonus = self.skill
        else:
            hitBonus = 0

        hitResult = self.hitContest(attack, hitBonus, creature)

        dmg_stat = self.stat['STR']
        if attack.from_weapon is not None:
            if attack.from_weapon.is_finesse:
                dmg_stat *= 1 + (self.stat['DEX'] - 25) / 100
            if attack.from_weapon.is_magic:
                dmg_stat = self.stat['WIT']

        if self.has_Trait('Charged_hits'):
            dmg_mult = 1 + self.movement / 100
        elif self.has_Trait('Savage_critical') and hitResult == 2:
            dmg_mult = 2
        else:
            dmg_mult = 1

        hitStatus = ''
        if hitResult > 0:
            if hitResult == 1:
                is_critical = False
            else:
                is_critical = True
                hitStatus = 'Critical: '
            damage = attack.rollDamage(dmg_stat, dmg_mult)
            appliedDamage = 0
            is_AP = attack.from_weapon.is_AP
            if creature.equippedArmour['Over'] is not None:
                if creature.equippedArmour['Over'].material == 'mail' and attack.from_weapon.is_fine:
                    is_AP = True
            appliedDamage += creature.take_damage(damage[attack.damage_maintype], attack.damage_maintype,
                                                 is_AP, is_critical, AA_stat)
            for damage_type in damage:  # Apply other (non-main) damage types associated with the attack
                if damage_type == attack.damage_maintype:
                    continue
                if appliedDamage > 0:
                    is_critical = True
                appliedDamage += creature.take_damage(damage[damage_type], damage_type,
                                                     is_AP, is_critical, AA_stat)

            indicator = hitStatus + str(appliedDamage)
        else:
            indicator = 'Blocked' if hitResult == 0 else 'Miss'

        return indicator

    # Makes an attack against another entity with the given attacks
    def attack(self, attackIDList, creature):
        indicatorList = []

        for attackID in attackIDList:
            indicator = self.singleAttack(attackID, creature)
            indicatorList.append(indicator)

        self.actions -= 1

        return indicatorList

    # Checks if entity is still alive
    def check_alive(self):
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
        if self.health > self.max_health:
            self.health = self.max_health
            
    # Resets the stats to the base stats
    def resetStats(self):
        for stat in self.base_stat:
            self.stat[stat] = self.base_stat[stat]
        
    def refreshMovement(self):
        self.movement = self.max_movement

    # Recalculates the entity damage and reach
    def refreshStatAfterWeapon(self):

        self.resetEvasion()
        self.reach = self.base_reach
        self.range = self.base_reach
        self.getAttackOptions()

        for hand in self.equipped_weapons:
            eq_weapon = self.equipped_weapons[hand]
            if eq_weapon is None:
                continue
            if eq_weapon.is_melee:
                if eq_weapon.range > self.reach:
                    self.reach = eq_weapon.range
            if eq_weapon.range > self.range:
                self.range = eq_weapon.range
            if eq_weapon.defense_type:
                protection = eq_weapon.protection
                if self.is_Proficient(eq_weapon):
                    protection *= 2
                self.evasion['Melee'] += protection
                if eq_weapon.defense_type == 'shield':
                    self.evasion['Ranged'] += protection

    # Resets evasion
    def resetEvasion(self):
        self.evasion['Melee'] = self.base_evasion
        self.evasion['Ranged'] = self.base_evasion

    def refreshStatAfterEquipment(self):
        self.refreshStatAfterArmour()
        self.calcEvasion()
        self.refreshStatAfterWeapon()
        if self.has_Trait('Tank'):
            armour_values = [self.armour[a_type] for a_type in self.armour]
            self.stat['CON'] += max(armour_values)

    # Recalculates the entity AC
    def refreshStatAfterArmour(self):

        if self.has_Trait('Armour_experience'):
            max_movement_reduction = 5
        else:
            max_movement_reduction = 30  # A number larger than the armour movement reductions

        self.bulk = 0
        self.stat['DEX'] = self.base_stat['DEX']
        for dmg_type in self.armour:
            self.armour[dmg_type] = self.base_armour
        self.max_movement = self.base_movement
        self.coverage = self.base_coverage

        total_flex = 1
        total_weight = 0
        for armour_type in self.equipped_armour:
            eq_armour = self.equipped_armour[armour_type]
            if eq_armour is None:
                continue

            material = eq_armour.material
            value = eq_armour.value

            total_flex *= eq_armour.flex
            total_weight += eq_armour.weight if not self.has_Trait('Light') else eq_armour.weight * 2
            self.coverage += eq_armour.coverage / 100
            self.bulk += eq_armour.bulk

            if material == 'cloth':
                self.armour['slashing'] += value
                self.armour['piercing'] += 0.5 * value
                self.armour['bludgeoning'] += value
            elif material == 'mail':
                self.armour['slashing'] += value
                self.armour['piercing'] += 0.5 * value
            elif material == 'plate':
                self.armour['slashing'] += value
                self.armour['piercing'] += 0.75 * value
                self.armour['bludgeoning'] += 0.5 * value

        if self.coverage > 1:
            self.coverage = 1

        self.armour['slashing'] = int(self.armour['slashing'])
        self.armour['piercing'] = int(self.armour['piercing'])
        self.armour['bludgeoning'] = int(self.armour['bludgeoning'])

        self.stat['DEX'] = self.stat['DEX'] ** total_flex
        if self.is_exceededBulk():
            self.stat['DEX'] = round(self.stat['DEX'])

        self.max_movement -= min(total_weight, max_movement_reduction)

    # Calculates the new evasion after a stat change
    def calcEvasion(self):
        self.base_evasion = self.stat['DEX']

    # Returns if the character exceeds their max bulk
    def is_exceededBulk(self) -> bool:
        return False

    # Makes a saving throw
    def makeSavingThrow(self):
        throw = rd.randint(1, 20)
        saved = False
        dies = False
        
        if throw == 1:
            self.saving_throws = (self.saving_throws[0], self.saving_throws[1]+2)
            output = 'Critical Fail'
        elif throw < 10:
            self.saving_throws = (self.saving_throws[0], self.saving_throws[1]+1)
            output = 'Fail'
        elif throw == 20:
            saved = True
            output = 'Critical Success!'
        else:
            self.saving_throws = (self.saving_throws[0]+1, self.saving_throws[1])
            output = 'Success!'
            
        if self.saving_throws[0] >= 3:
            saved = True
        elif self.saving_throws[1] >= 3:
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
        for hand in self.equipped_weapons:
            if self.equipped_weapons[hand] is not None:
                self.equipped_weapons[hand] = self.__weapon_factory.create(self.equipped_weapons[hand])
        for armour_type in self.equipped_armour:
            if self.equipped_armour[armour_type] is not None:
                self.equipped_armour[armour_type] = it.Armour(self.equipped_armour[armour_type])

        self.createInventory()

    # Converts the list of base attacks from strings to classes
    def convAttacks(self):
        new_list = []
        for i, attack_str in enumerate(self.base_attacks):
            attack = self.__attack_factory.create(attack_str)
            attack.id = i
            new_list.append(attack)
        self.base_attacks = new_list

    # Gets what attacks are available and adds them to the options list - also ids them
    def getAttackOptions(self):
        i = 0
        self.attack_options = []
        for location in self.equipped_weapons:
            weapon = self.equipped_weapons[location]
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
            item = self.__weapon_factory.create(item_str)  # Converts to weapon for now
            new_list.append(item)
        self.inventory = new_list

    # Functions to be redefined with npc and player classes
    def is_Proficient(self, weapon: it.Weapon):
        pass