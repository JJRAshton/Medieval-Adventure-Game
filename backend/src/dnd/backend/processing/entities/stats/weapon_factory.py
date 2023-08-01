from .make_dataframes import EntityStatDictionaryProvider
from ....utils import dice_utils
from ..item import Weapon, Armour
from .attack_factory import AttackFactory

WEAPON_TRAITS = ['Ranged', 'Loading','Two-handed', 'Arrows', 'Bolts',
                 'Light', 'Finesse', 'Armour Piercing', 'Fine', 'Magic', 'Melee']

class WeaponFactory:

    def __init__(self, stat_provider: EntityStatDictionaryProvider, attack_factory: AttackFactory):
        self.__stat_provider = stat_provider
        self.__attack_factory = attack_factory
    
    def create(self, weapon_name: str) -> Weapon:
        ''' Creates a weapon '''
        wep_dict = self.__stat_provider.get_weapon_stats_dict(weapon_name)

        attacks_list = [self.__attack_factory.create(attack_str) for attack_str in dice_utils.convertList(wep_dict['Attacks'])]

        weapon = Weapon(
            weaponName = weapon_name,
            damage_dice = int(wep_dict['Damage Dice'][1:]) if wep_dict['Damage Dice'] else 0,
            attack_range = int(wep_dict['Range']),
            attacks = attacks_list,
            protection = int(wep_dict['Protection']) if wep_dict['Protection'] else 0,
            defense_type = wep_dict['Defense Type'] if wep_dict['Protection'] else '',
            traits = [trait for trait in WEAPON_TRAITS if wep_dict[trait]]
        )
        
        # This is a bit ugly, and can probably be avoided with a bit more thought
        weapon.type = wep_dict['Type']
        for attack in attacks_list:
            attack.setWeapon(weapon)
            attack.updateDamage()

        return weapon
    
    def create_armour(self, armour_name) -> Armour:
        armour = Armour(armour_name)
        self.getArmourStats(armour)
        return armour

    def getArmourStats(self, armour: Armour):
        arDict = self.__stat_provider.get_armour_stats_dict(armour.name)

        armour.type = arDict['Type']
        armour.material = arDict['Material']
        armour.bulk = int(arDict['Bulk'])
        armour.coverage = int(arDict['Coverage'])
        armour.value = int(arDict['Armour Value'])
        armour.flex = int(arDict['Flex']) / 100
        armour.weight = int(arDict['Movement Penalty'])
