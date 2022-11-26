import random as rd

import backend.processing as pr


class Arena:
    def __init__(self):
        self.arena_back = None

        self.classes = ['Raider', 'Gladiator', 'Ranger', 'Knight', 'Hunter', 'Professor', 'Ninja']
        self.no = len(self.classes)

        self.players = []

        self.backs = 0

        self.r_points = []
        self.points = [0 for _ in range(self.no)]
        self.entries = [0 for _ in range(self.no)]

        self.avStat = [0 for _ in range(4)]
        self.avHealth = [0 for _ in range(self.no)]

        self.newBack()

    # One entity fights another to the death at random
    def duel(self):
        player1, player2 = rd.sample(self.players, 2)
        self.entries[player1.id] += 1
        self.entries[player2.id] += 1

        # print('People:', player1.type, player2.type)
        while player1.health > 0 and player2.health > 0:
            player1.attack([0], player2)
            # print(player1.health, player2.health)
            player2.attack([0], player1)

        if player1.health > 0:
            self.points[player1.id] += 1
            # print('Winner:', player1.type, self.points[player1.id])
        elif player2.health > 0:
            self.points[player2.id] += 1
            # print('Winner:', player2.type, self.points[player2.id])
        else:
            self.points[player1.id] += 0.5
            self.points[player2.id] += 0.5
            # print('Draw')

        player1.refreshHealth()
        player2.refreshHealth()
        # print(player1.maxHealth - player1.health, player2.maxHealth - player2.health)

    def displayStats(self, character_id):
        character = self.players[character_id]

        print('     STR:', character.stat['STR'], 'DEX:', character.stat['DEX'], 'CON:', character.stat['CON']
              , 'WIT:', character.stat['WIT'])
        print('     Evasion:', character.evasion['Melee']['slashing'], character.evasion['Ranged'])
        print('     Armour:', character.armour)
        print('     Health:', character.maxHealth)

    def newBack(self):
        self.backs += 1
        self.arena_back = pr.Back(1, self.no)
        self.r_points = [0 for _ in range(len(self.players))]

        self.players = self.arena_back.characters

        for x, stat in enumerate(self.players[0].stat):
            self.avStat[x] += self.players[0].stat[stat]

        for x in range(len(self.players)):
            self.avHealth[x] += self.players[x].maxHealth

    def returnStat(self, classes):
        stat = [round(self.avStat[x] / self.backs, 2) for x in range(len(self.avStat))]
        stat.sort(reverse=True)
        print('Stats:', stat)

        hp = [round(self.avHealth[x] / self.backs, 2) for x in range(len(self.avHealth))]
        zipped_hp = zip(classes, hp)
        print('HP:', list(zipped_hp))

    def calcWR(self):
        for _ in range(1000):
            for _ in range(10):
                self.duel()

            self.newBack()

        wr = [round(self.points[x] / self.entries[x], 2) for x in range(len(self.points))]
        zipped_wins = zip(self.classes, self.points)
        zipped_wr = zip(self.classes, wr)
        self.returnStat(self.classes)
        print('Wins:', list(zipped_wins))
        print('WR: ', list(zipped_wr))


if __name__ == '__main__':
    comparison_arena = Arena()
    comparison_arena.calcWR()
