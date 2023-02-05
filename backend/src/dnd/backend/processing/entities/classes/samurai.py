from .player_class import Class


class Samurai(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Samurai'
        self.stat_order = ['STR', 'DEX', 'WIT', 'CON']
        self.weapons = ['single_edged_swords']  # bows
        self.traits = ['Melee_evader', 'Keen_eye']

        self.getStats()
