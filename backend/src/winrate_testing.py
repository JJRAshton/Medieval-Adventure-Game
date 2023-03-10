from .dnd.arena import Arena


if __name__ == '__main__':
    classes = ['Raider', 'Gladiator', 'Guardian', 'Knight', 'Samurai', 'Hunter']  # Professor
    comparison_arena = Arena(classes)
    comparison_arena.calcWR()
    # comparison_arena.displayStats(3)
    # comparison_arena.displayStats(5)
