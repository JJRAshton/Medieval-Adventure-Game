from .make_dataframes import AttackStatDictionaryProvider
from . import dice_utils
from ..attack import Attack


class AttackFactory:

    ''' Attack factory '''
    def __init__(self, stat_provider: AttackStatDictionaryProvider):
        self.__attack_stat_provider = stat_provider

    def create(self, attack_name: str) -> Attack:
        ''' Create an attack '''
        attack = Attack(attack_name)
        if attack_name in self.__attack_stat_provider.weapon_attacks.index.tolist():
            self.__assign_weapon_attack_stats(attack)
        elif attack_name in self.__attack_stat_provider.raw_attacks.index.tolist():
            self.__assign_raw_attack_stats(attack)
        else:
            raise ValueError(f"Attack with name {attack_name} was not recognised")
        return attack
    
        
    
    def __assign_weapon_attack_stats(self, attack):
        ''' Create an attack from a weapon '''
        atkDict = self.__attack_stat_provider.get_weapon_attack_stats_dict(attack.name)
        attack.type = 'weapon'

        dmg_type1 = atkDict['Dmg Typ 1']
        attack.damage_types[dmg_type1] = float(atkDict['Fraction 1'])
        attack.damage_maintype = dmg_type1
        if atkDict['Dmg Typ 2']:
            dmg_type2 = atkDict['Dmg Typ 2']
            attack.damage_types[dmg_type2] = 1 - float(atkDict['Fraction 1'])

        attack.damage = (int(atkDict['Dice No.']), 0)

    def __assign_raw_attack_stats(self, attack):
        ''' Create an innate attack '''
        atkDict = self.__attack_stat_provider.get_raw_attack_stats_dict(attack.name)
        attack.type = 'raw'

        dmg_type1 = atkDict['Dmg Typ 1']
        attack.damage_types[dmg_type1] = int(atkDict['Fraction 1'])
        if atkDict['Dmg Typ 2']:
            dmg_type2 = atkDict['Dmg Typ 2']
            attack.damage_types[dmg_type2] = 1 - int(atkDict['Fraction 1'])

        attack.damage = dice_utils.convertDice(atkDict['Damage'])
