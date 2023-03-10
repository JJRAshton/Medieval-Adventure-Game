import random as rd
from sortedcontainers import SortedList

import stats_loader as sl
"""Keeps Track of Creature Healths and Initiative Order in Combat"""


# Rolls n dice of d sides
def roll(n, d):
    total = 0
    for i in range(n):
        total += rd.randint(1, d)
    return total


# Creature class for containing all creature parameters
class Creature:
    def __init__(self, stats, colour=None):
        self.stats = stats

        if self.ctype != 'player':
            n = self.stats['Level']
            d = self.stats['Hit_Dice']
            b = n*self.stats['CON']

            self.hp = roll(n, d)+b
            self.temp_hp = 0

            self.colour = colour

    # Updates the health of a creature: type1=damage, type2=heal, type3=temphp
    def updateHealth(self, hp_change, hp_type=1):
        # Damages the creature
        if hp_type == 1:
            if hp_change >= self.temp_hp:
                excess_damage = hp_change - self.temp_hp
                self.tempHP = 0
                self.hp -= excess_damage
            else:
                self.tempHP -= hp_change

        # Heals the creature
        elif hp_type == 2:
            self.hp += hp_change

        elif hp_type == 3:
            self.temp_hp = hp_change


# Creatures bundled into one group for initiative
class CreatureGroup:
    # Magnet Colours
    colours = ['red', 'blue', 'yellow', 'orange', 'green']

    def __init__(self, c_type, group_size, init, group_no=''):
        self.c_type = c_type
        self.size = group_size
        self.stats = sl.creature_stats[self.c_type]

        self.name = c_type + group_no

        self.members = []

        self.init = init

        self.create()

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.init > other.init

    def __str__(self):
        return self.name

    # Rolls initiative
    def init_roll(self):
        return roll(1, 20) + self.stats['DEX']

    # Creates the group from given creature type and group size
    def create(self):

        if self.size > len(CreatureGroup.colours):
            raise ValueError

        for i in range(self.size):
            colour = CreatureGroup.colours[i]

            new_creature = Creature(self.stats, colour)

            self.members.append(new_creature)


# Player for initiative order
class Player:

    def __init__(self, name, init):
        self.name = name
        self.init = init

        self.c_type = 'player'

    def __lt__(self, other):
        return self.init > other.init

    def __str__(self):
        return self.name


# Calculator for initialising
class Calculator:

    def __init__(self):
        self.groups = []
        self.initiative_order = SortedList()

        self.reroll_list = []  # Unused

    # Arranges many creatures into groups
    def arrange(self, c_type, c_number, n_groups, team):

        # Finds the two group sizes for if the number does not divide evenly
        remainder = c_number % n_groups
        group_size_n = (c_number - remainder) / n_groups

        group_sizes_lrg = [group_size_n+1 for _ in range(remainder)]
        group_sizes_sml = [group_size_n for _ in range(n_groups - remainder)]

        group_sizes = group_sizes_lrg + group_sizes_sml

        # Name group with a number if there are multiple groups
        num_name = n_groups > 1

        for i, sz in enumerate(group_sizes):
            group_no = str(i) if num_name else ''

            group = CreatureGroup(c_type, sz, team, group_no)
            self.groups.append(group)

    # Adds a player to the groups
    def add_player(self, name, init):

        player = Player(name, init)

        self.groups.append(player)

    # Makes the initiative order
    def order_initiative(self):

        for group in self.groups:
            self.initiative_order.add(group)

    # Checks for any initiative roll duplicates
    def check_initiative(self):

        for i in range(len(self.initiative_order)-1):
            if self.initiative_order[i].init == self.initiative_order[i+1].init:
                reroll = [i, i+1]
                self.reroll_list.append(reroll)
