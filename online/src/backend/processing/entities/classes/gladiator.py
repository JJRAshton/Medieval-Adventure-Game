from .player_class import Class


class Gladiator(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Gladiator'
        self.stat_order = ['STR', 'DEX', 'CON', 'WIT']
        self.weapons = ['spears', 'clubs', 'heavy_throwables']
        self.health_modifier = 2
