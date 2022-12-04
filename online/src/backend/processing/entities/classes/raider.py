from .player_class import Class


class Raider(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Raider'
        self.stat_order = ['STR', 'CON', 'DEX', 'WIT']
        self.weapons = ['glaives', 'axes', 'heavy_throwables']  # glaives
        self.traits = ['Charger', 'Light']

        self.getStats()
