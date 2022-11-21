import random as rd


# Rolls for the damage to an entity
def rollDamage(attack, dmg_stat):
    number, dice = attack.damage

    # Roll for base damage
    base = 0
    for _ in range(number):
        base += rd.randint(1, dice)

    # Increases it according to the damage stat
    totalDamage = base * (1+dmg_stat/100)

    damage = {}
    for damage_type in attack.damage_types:
        damage[damage_type] = totalDamage * attack.damage_types[damage_type]

    return damage
