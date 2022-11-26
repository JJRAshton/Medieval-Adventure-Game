from .player_class import Class


class Hunter(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Hunter'
        self.stat_order = ['DEX', 'STR', 'WIT', 'CON']
        self.weapons = ['bows', 'crossbows', 'axes']