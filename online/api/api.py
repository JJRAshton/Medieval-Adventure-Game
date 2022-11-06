class APIAttack:

    def __init__(self, attacker, attacked, weapon):
        self.attacker = attacker
        self.attacked = attacked
        self.weapon = weapon

class APIMove:

    def __init__(self, entity, dest):
        self.entity = entity
        self.dest = dest

class APIEntity:

    def __init__(self, health, attackBonus, armourClass):
        self.health = health
        self.attackBonus = attackBonus
        self.armourClass = armourClass

class APIWeapon:

    def __init__(self, range, dice):
        self.range = range
        self.dice = dice