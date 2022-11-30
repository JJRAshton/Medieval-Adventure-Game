from .player_class import Class


class Hunter(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Hunter'
        self.stat_order = ['STR', 'DEX', 'WIT', 'CON']
        self.weapons = ['special', 'axes']  # bows

        self.getStats()
