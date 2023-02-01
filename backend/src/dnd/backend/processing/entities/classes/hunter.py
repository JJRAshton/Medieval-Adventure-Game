from .player_class import Class


class Hunter(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Hunter'
        self.stat_order = ['WIT', 'DEX', 'STR', 'CON']
        self.weapons = ['special', 'axes']  # bows
        self.traits = ['Ranged_evader', 'Melee_evader']

        self.getStats()
