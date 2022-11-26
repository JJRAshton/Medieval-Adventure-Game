from .player_class import Class


class Knight(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Knight'
        self.stat_order = ['CON', 'STR', 'WIT', 'DEX']
        self.weapons = ['hybrids', 'double_edged_swords', 'shields']