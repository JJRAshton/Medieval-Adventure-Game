from .player_class import Class


class Ninja(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Ninja'
        self.stat_order = ['DEX', 'WIT', 'STR', 'CON']
        self.weapons = ['single_edged_swords', 'light_throwables', 'mythical']
        self.traits = ['Melee_evader']

        self.getStats()
