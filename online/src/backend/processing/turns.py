from sortedcontainers import SortedList


class Time:

    def __init__(self, given_back):
        self.back = given_back
        self.initOrder = SortedList()

        self.is_combat = True

        self.winning_team = 0  # 1: Players, 2: Monsters

    # Starts the games turns
    def start(self):

        for character in self.back.characters:
            self.initOrder.add(character)

        self.loop()

    # The combat round/turn loop
    def loop(self):

        while self.is_combat:

            for n_round, character in enumerate(self.initOrder, start=1):
                if not character.is_alive:
                    continue

                character.initialiseTurn()

                if character.behaviour_type == 1:
                    self.playerTurn(character)

                if character.behaviour_type == 2:
                    self.npcTurn(character)

            self.checkCombat()

    # Checks if combat is still taking place
    def checkCombat(self):

        # Check if any players are still alive
        is_a_player = False
        for player in self.back.players:
            player_down = not player.is_conscious or not player.is_alive
            is_a_player = is_a_player or not player_down
        if not is_a_player:
            self.winning_team = 2
            self.is_combat = False

        # Check if any monsters are still alive
        is_a_monster = False
        for npc in self.back.characters:
            if npc.team == 2:
                is_a_monster = is_a_monster or npc.is_alive
        if not is_a_monster:
            self.winning_team = 1
            self.is_combat = False

    # Gets a player to make their turn
    def playerTurn(self, character):
        if not character.is_conscious:
            outcome = character.makeSavingThrow()
        pass

    # Gets an NPC to make their turn
    def npcTurn(self, character):
        if not character.is_conscious:
            outcome = character.makeSavingThrow()
        pass
