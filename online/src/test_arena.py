import random as rd

import backend.processing as pr


class Arena:
    def __init__(self, nPlayers):
        self.arena_back = pr.Back(1, nPlayers)

        self.players = self.arena_back.characters

        self.points = [0 for _ in range(len(self.players))]
        self.entries = [0 for _ in range(len(self.players))]

    # One entity fights another to the death at random
    def duel(self):
        player1, player2 = rd.sample(self.players, 2)
        self.entries[player1.id] += 1
        self.entries[player2.id] += 1

        print('People:', player1.type, player2.type)
        while player1.health > 0 and player2.health > 0:
            player1.attack([0], player2)
            # print(player1.health, player2.health)
            player2.attack([0], player1)

        print(player1.health, player2.health)

        if player1.health > 0:
            self.points[player1.id] += 1
            print('Winner:', player1.type, self.points[player1.id])
        elif player2.health > 0:
            self.points[player2.id] += 1
            print('Winner:', player2.type, self.points[player2.id])
        else:
            self.points[player1.id] += 0.5
            self.points[player2.id] += 0.5
            print('Draw')
        print(player1.maxHealth - player1.health, player2.maxHealth - player2.health)

    def displayStats(self, character_id):
        character = self.players[character_id]

        print('     STR:', character.stat['STR'], 'DEX:', character.stat['DEX'], 'CON:', character.stat['CON']
              , 'WIT:', character.stat['WIT'])
        print('     Evasion:', character.evasion['Melee']['slashing'], character.evasion['Ranged'])
        print('     Armour:', character.armour)
        print('     Health:', character.maxHealth)


if __name__ == '__main__':
    arena = Arena(5)
    classes = ['Beserker', 'Gladiator', 'Ranger', 'Knight', 'Samurai']

    for _ in range(10):
        arena.duel()

    wr = [round(arena.points[x] / arena.entries[x], 2) for x in range(len(arena.players))]
    zipped_entry = zip(classes, arena.entries)
    zipped_wins = zip(classes, arena.points)
    zipped_wr = zip(classes, wr)
    print('Fought:', list(zipped_entry))
    print('Wins:', list(zipped_wins))
    print('WR: ', list(zipped_wr))
    for num in range(5):
        print(classes[num])
        arena.displayStats(num)
