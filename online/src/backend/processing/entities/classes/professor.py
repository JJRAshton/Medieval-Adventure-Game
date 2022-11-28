from .player_class import Class


class Professor(Class):

    def __init__(self):
        super().__init__()
        self.name = 'Professor'
        self.stat_order = ['WIT', 'DEX', 'CON', 'STR']
        self.weapons = ['staves', 'books', 'mythical']

        self.getStats()
