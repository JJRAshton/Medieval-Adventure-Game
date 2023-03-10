import random as rd
import copy

from .backend import processing as pr


class Arena:
    def __init__(self, classes):
        self.arena_back = None

        self.classes = classes  # ['Raider', 'Gladiator', 'Guardian', 'Knight', 'Hunter', 'Professor', 'Ninja']
        self.creatures = []
        self.no = len(self.classes) + len(self.creatures)

        self.players = []

        self.backs = 0

        self.r_points = []
        self.points = [0 for _ in range(self.no)]
        self.wins = [0 for _ in range(self.no)]
        self.entries = [0 for _ in range(self.no)]

        self.avStat = [0 for _ in range(4)]
        self.avHealth = [0 for _ in range(self.no)]

        self.newBack()

    # One entity fights another to the death at random
    def duel(self, log=False):
        player1, player2 = rd.sample(self.players, 2)
        self.entries[player1.id] += 1
        self.entries[player2.id] += 1

        max_count = 1000
        count = 0
        player1_str = player1.p_class.name
        player2_str = player2.p_class.name
        if log:
            print('People:', player1_str, player2_str)
        while player1.health > 0 and player2.health > 0 and count < max_count:
            for action in range(player1.actionsTotal):
                if log:
                    print(f'{player1_str} swings')
                indicators = player1.attack([0], player2)
                if log:
                    print(f'Result: {indicators[0]}')
            if player2.health == 0:
                break
            for action in range(player2.actionsTotal):
                if log:
                    print(f'{player2_str} swings')
                indicators = player2.attack([0], player1)
                if log:
                    print(f'Result: {indicators[0]}')
            if log:
                print('Remaining healths -', f'{player1_str}: {player1.health}', f'{player2_str}: {player2.health}')
            count += 1

        if player2.health == 0 and player1.health > 0:
            self.points[player1.id] += 1
            self.wins[player1.id] += 1
            if log:
                print('Winner:', player1_str)
        elif player1.health == 0 and player2.health > 0:
            self.points[player2.id] += 1
            self.wins[player2.id] += 1
            if log:
                print('Winner:', player2_str)
        else:
            self.points[player1.id] += 0.5
            self.points[player2.id] += 0.5
            if log:
                print('Draw')

        if log:
            self.displayStats(player1.id)
            self.displayStats(player2.id)

        player1.refreshHealth()
        player2.refreshHealth()

    def displayStats(self, character_id):
        character = self.players[character_id]
        print(f'Stats for {character.p_class.name}')

        print('     STR:', character.stat['STR'], 'DEX:', character.stat['DEX'], 'CON:', character.stat['CON']
              , 'WIT:', character.stat['WIT'])
        print('     Evasion:', character.evasion['Melee'], character.evasion['Ranged'])
        print('     Armour:', character.armour)
        print('     Bulk:', character.bulk)
        print('     Max Bulk:', character.p_class.max_bulk)
        print('     Health:', character.maxHealth)
        if character.equippedWeapons['Left'] or character.equippedWeapons['Right']:
            left_weapon = None
            right_weapon = None
            if character.equippedWeapons['Left']:
                left_weapon = character.equippedWeapons['Left'].name
            if character.equippedWeapons['Right']:
                right_weapon = character.equippedWeapons['Right'].name
            print('     Weapon:', left_weapon, right_weapon)
        elif character.equippedWeapons['Both']:
            print('     Weapon:', character.equippedWeapons['Both'].name)

    def newBack(self):
        self.backs += 1
        classes = copy.copy(self.classes)
        self.arena_back = pr.Back(1, len(classes), 1, classes)
        self.r_points = [0 for _ in range(len(self.players))]

        self.players = self.arena_back.characters

        for x, stat in enumerate(self.players[self.no-1].stat):
            self.avStat[x] += self.players[self.no-1].stat[stat]

        for x in range(len(self.players)):
            self.avHealth[x] += self.players[x].maxHealth

    def returnStat(self, classes):
        stat = [round(self.avStat[x] / self.backs, 2) for x in range(len(self.avStat))]
        stat.sort(reverse=True)
        print('Stats:', stat)

        hp = [round(self.avHealth[x] / self.backs, 2) for x in range(len(self.avHealth))]
        zipped_hp = zip(classes, hp)
        print('HP:', list(zipped_hp))

    def calcWR(self, generations=1000, pairings=10):
        for _ in range(generations):
            for _ in range(pairings):
                self.duel()

            self.newBack()

        classes = copy.copy(self.classes)
        wr = [round(self.points[x] / self.entries[x], 2) for x in range(len(self.points))]
        names = self.creatures + classes
        zipped_wins = zip(names, self.wins)
        zipped_points = zip(names, self.points)
        zipped_wr = zip(names, wr)
        self.returnStat(names)
        print('Points:', list(zipped_points))
        print('Wins:', list(zipped_wins))
        print('WR: ', list(zipped_wr))