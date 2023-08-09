from .make_dataframes import AttackStatDictionaryProvider
from ....utils import dice_utils
from ..attack import Attack, AttackType, AttackTypes


class AttackFactory:

    ''' Attack factory '''
    def __init__(self, stat_provider: AttackStatDictionaryProvider):
        self.__attack_stat_provider = stat_provider

    def create(self, attack_name: str) -> Attack:
        ''' Create an attack '''
        if attack_name in self.__attack_stat_provider.weapon_attacks.index.tolist():
            return self.__create_internal(attack_name, AttackTypes.WEAPON)
        elif attack_name in self.__attack_stat_provider.raw_attacks.index.tolist():
            return self.__create_internal(attack_name, AttackTypes.RAW)
        else:
            raise ValueError(f"Attack with name {attack_name} was not recognised")

    def __create_internal(self, attack_name: str, attack_type: AttackType) -> Attack:
        ''' Create an attack from a weapon '''
        if attack_type == AttackTypes.WEAPON:
            atkDict = self.__attack_stat_provider.get_weapon_attack_stats_dict(attack_name)
            damage=(int(atkDict['Dice No.']), 0)
        else:
            atkDict = self.__attack_stat_provider.get_raw_attack_stats_dict(attack_name)
            damage=dice_utils.convertDice(atkDict['Damage'])
            
        return Attack(
            atk_name=attack_name,
            attack_type=attack_type.get_name(),
            damage=damage,
            damage_types={
                atkDict['Dmg Typ 1']: float(atkDict['Fraction 1']),
                atkDict['Dmg Typ 2']: 1 - float(atkDict['Fraction 1'])
            },
            damage_maintype=atkDict['Dmg Typ 1'])
