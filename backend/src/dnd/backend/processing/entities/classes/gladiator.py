from .player_class import Class


class Gladiator(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Gladiator'
        self.stat_order = ['STR', 'DEX', 'CON', 'WIT']
        self.weapons = ['arena_weapons', 'heavy_throwables']
        self.traits = ['Keen_eye', 'Savage_critical']

        self.getStats()
