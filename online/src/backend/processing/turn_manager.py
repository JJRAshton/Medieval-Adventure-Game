from sortedcontainers import SortedList


class TurnManager:

    def __init__(self, given_back, turn_notifier):
        self.back = given_back
        self.initOrder = SortedList()
        self.turn_notifier = turn_notifier

        self.is_combat = True
        self.started = False

        self.winning_team = 0  # 1: Players, 2: Monsters

    def get_on_turn_id(self):
        if not self.started:
            raise RuntimeError("Game has not started")
        return self.on_turn

    # Starts the games turns
    def start(self):
        # Probably this could all go into the init
        for character in self.back.characters:
            self.initOrder.add(character)

        if len(self.initOrder) == 0:
            raise RuntimeError("Started game with no players?")

        self.started = True
        self._on_turn_index = 0
        self.on_turn_id = self.initOrder[self._on_turn_index].id
        self.turn_notifier.announce(self.on_turn_id, self.initOrder[self._on_turn_index].behaviour_type == 1)

    def endTurn(self):
        # This resets the previous player at the end of their turn
        self.initOrder[self._on_turn_index].initialiseTurn()

        self._on_turn_index += 1
        self._on_turn_index %= len(self.initOrder) # It is unsafe to add and remove players

        on_turn_character = self.initOrder[self._on_turn_index]
        # on_turn_character.initialiseTurn()
        self.on_turn_id = on_turn_character.id

        if on_turn_character.is_alive:
            if not on_turn_character.is_conscious and not on_turn_character.is_stable:
                on_turn_character.makeSavingThrow()

            self.turn_notifier.announce(on_turn_character.id, on_turn_character.behaviour_type == 1)
        else:
            # If the next player is dead, we skip turn immediately
            self.endTurn()

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