from .make_dataframes import ENTITY_STAT_PROVIDER
from ....utils import dice_utils
from ..item import Weapon, Armour
from .attack_factory import AttackFactory
from ...id_generator import IDGenerator

WEAPON_TRAITS = ['Ranged', 'Loading','Two-handed', 'Arrows', 'Bolts',
                 'Light', 'Finesse', 'Armour Piercing', 'Fine', 'Magic', 'Melee']

class WeaponFactory:

    def __init__(self, attack_factory: AttackFactory, id_generator: IDGenerator):
        self.__attack_factory = attack_factory
        self.__id_generator = id_generator
    
    def create(self, weapon_name: str) -> Weapon:
        ''' Creates a weapon '''
        wep_dict = ENTITY_STAT_PROVIDER.get_weapon_stats_dict(weapon_name)

        attacks_list = [self.__attack_factory.create(attack_str) for attack_str in dice_utils.convertList(wep_dict['Attacks'])]

        weapon = Weapon(
            weaponName = weapon_name,
            id=self.__id_generator.get_item_id(),
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
    
    def create_armour(self, armour_name: str) -> Armour:
        armour_dict = ENTITY_STAT_PROVIDER.get_armour_stats_dict(armour_name)
        armour = Armour(
            armourName = armour_name,
            id=self.__id_generator.get_item_id(),
            armour_type = armour_dict['Type'],
            value = int(armour_dict['Armour Value']),
            flex = int(armour_dict['Flex']) / 100,
            weight = int(armour_dict['Movement Penalty']),
            material = armour_dict['Material'],
            coverage = int(armour_dict['Coverage']),
            bulk = int(armour_dict['Bulk'])
        )
        return armour