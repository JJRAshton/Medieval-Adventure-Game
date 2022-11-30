from arena import Arena


if __name__ == '__main__':
    classes = ['Raider', 'Gladiator', 'Guardian', 'Knight', 'Hunter', 'Ninja']  # Professor
    comparison_arena = Arena(['Guardian', 'Ninja'])
    comparison_arena.duel(log=True)
    # comparison_arena.displayStats(0)
    # comparison_arena.displayStats(1)
