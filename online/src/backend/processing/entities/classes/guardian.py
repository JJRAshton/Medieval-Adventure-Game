from .player_class import Class


class Guardian(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Guardian'
        self.stat_order = ['CON', 'WIT', 'STR', 'DEX']
        self.weapons = ['books', 'shields', 'hammers']
        self.health_modifier = 2
