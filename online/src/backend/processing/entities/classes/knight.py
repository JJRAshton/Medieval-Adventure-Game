from .player_class import Class


class Knight(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Knight'
        self.stat_order = ['STR', 'CON', 'WIT', 'DEX']
        self.weapons = ['polearms', 'double_edged_swords', 'spears']
        self.health_modifier = 1.6
