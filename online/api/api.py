class APIWeapon:

    def __init__(self, range, dice):
        self.range = range
        self.dice = dice

class APILocation:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class APIEntity:

    def __init__(self, health, attackBonus, armourClass):
        self.health = health
        self.attackBonus = attackBonus
        self.armourClass = armourClass

class APIMove:

    def __init__(self, entity, dest):
        self.entity = entity
        self.dest = dest

class APIAttack:

    def __init__(self, attacker, attacked, weapon):
        self.attacker = attacker
        self.attacked = attacked
        self.weapon = weapon

class APIServer:

    def moveRequest(self, move: APIMove):
        raise NotImplementedError

    def attackRequest(self, attck: APIAttack):
        raise NotImplementedError