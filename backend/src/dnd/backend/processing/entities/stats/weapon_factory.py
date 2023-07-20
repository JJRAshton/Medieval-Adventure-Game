from .make_dataframes import EntityStatDictionaryProvider
from . import dice_utils
from ..item import Weapon
from .attack_factory import AttackFactory


class WeaponFactory:

    def __init__(self, stat_provider: EntityStatDictionaryProvider, attack_factory: AttackFactory):
        self.__stat_provider = stat_provider
        self.__attack_factory = attack_factory


    def __getWeaponDict(self, weaponName: str):
        weaponDict = self.__stat_provider.get_weapon_stats_dict(weaponName)
        return weaponDict
    
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

    def getWeaponStats(self, weapon: Weapon):   # Doesn't collect all data
        wepDict = self.__getWeaponDict(weapon.name)

        weapon.type = wepDict['Type']
        weapon.range = int(wepDict['Range'])
        if wepDict['Damage Dice']:
            weapon.damage_dice = int(wepDict['Damage Dice'][1:])

        weapon.attacks = dice_utils.convertList(wepDict['Attacks'])

        if wepDict['Ranged']:
            weapon.is_ranged = True
        if wepDict['Loading']:
            weapon.is_loading = True
        if wepDict['Two-handed']:
            weapon.is_twoHanded = True
        if wepDict['Arrows']:
            weapon.is_arrows = True
        if wepDict['Bolts']:
            weapon.is_bolts = True
        if wepDict['Light']:
            weapon.is_light = True
        if wepDict['Finesse']:
            weapon.is_finesse = True
        if wepDict['Armour Piercing']:
            weapon.is_AP = True
        if wepDict['Fine']:
            weapon.is_fine = True
        if wepDict['Magic']:
            weapon.is_magic = True
        if wepDict['Melee']:
            weapon.is_melee = False

        if wepDict['Protection']:
            weapon.protection = int(wepDict['Protection'])
            weapon.defense_type = wepDict['Defense Type']