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
        weapon = Weapon(weapon_name)
        self.getWeaponStats(weapon)
        attacks_list = []
        for attack_str in weapon.attacks:
            attack = self.__attack_factory.create(attack_str)
            attack.setWeapon(weapon)
            attack.updateDamage()
            attacks_list.append(attack)
        weapon.attacks = attacks_list
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


    def getWeaponStats(self, weapon: Weapon):   # Doesn't collect all data
        wepDict = self.__stat_provider.get_weapon_stats_dict(weapon.name)

        weapon.type = wepDict['Type']
        weapon.range = int(wepDict['Range'])
        if wepDict['Damage Dice']:
            weapon.damage_dice = int(wepDict['Damage Dice'][1:])

        weapon.attacks = dice_utils.convertList(wepDict['Attacks'])

        weapon.traits = [trait for trait in WEAPON_TRAITS if wepDict[trait]]

        if wepDict['Protection']:
            weapon.protection = int(wepDict['Protection'])
            weapon.defense_type = wepDict['Defense Type']