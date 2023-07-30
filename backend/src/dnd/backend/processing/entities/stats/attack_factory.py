from .make_dataframes import AttackStatDictionaryProvider
from ....utils import dice_utils
from ..attack import Attack, AttackType, AttackTypes


class AttackFactory:

    ''' Attack factory '''
    def __init__(self, stat_provider: AttackStatDictionaryProvider):
        self.__attack_stat_provider = stat_provider

    def create(self, attack_name: str) -> Attack:
        ''' Create an attack '''
        attack = Attack(attack_name)
        if attack_name in self.__attack_stat_provider.weapon_attacks.index.tolist():
            self.__assign_attack_stats(attack, AttackTypes.WEAPON)
        elif attack_name in self.__attack_stat_provider.raw_attacks.index.tolist():
            self.__assign_attack_stats(attack, AttackTypes.RAW)
        else:
            raise ValueError(f"Attack with name {attack_name} was not recognised")
        return attack
    
    def __assign_attack_stats(self, attack, attack_type: AttackType):
        ''' Create an attack from a weapon '''
        if attack_type == AttackTypes.WEAPON:
            atkDict = self.__attack_stat_provider.get_weapon_attack_stats_dict(attack.name)
        else:
            atkDict = self.__attack_stat_provider.get_raw_attack_stats_dict(attack.name)
        attack.type = attack_type.get_name()
        self.__set_damage_types(attack, atkDict)
        if attack_type == AttackTypes.WEAPON:
            attack.damage = (int(atkDict['Dice No.']), 0)
        else:
            attack.damage = dice_utils.convertDice(atkDict['Damage'])

    def __set_damage_types(self, attack: Attack, atkDict):
        dmg_type1 = atkDict['Dmg Typ 1']
        attack.damage_types[dmg_type1] = float(atkDict['Fraction 1'])
        attack.damage_maintype = dmg_type1
        if atkDict['Dmg Typ 2']:
            dmg_type2 = atkDict['Dmg Typ 2']
            attack.damage_types[dmg_type2] = 1 - float(atkDict['Fraction 1'])
