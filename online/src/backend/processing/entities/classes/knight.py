from .player_class import Class


class Knight(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Knight'
        self.stat_order = ['STR', 'CON', 'WIT', 'DEX']
        self.weapons = ['polearms', 'double_edged_swords']  # polearms, double_edged_swords, crossbows
        self.traits = ['Armour_expert']

        self.getStats()
