from .player_class import Class


class Ranger(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Ranger'
        self.stat_order = ['CON', 'WIT', 'DEX', 'STR']
        self.weapons = ['bows', 'double_edged_swords', 'special']