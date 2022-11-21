import random as rd


stat1 = 20
stat2 = 50

bonus1 = 25

n = 100000

crit_count = 0
count = 0
for i in range(n):
    roll1 = rd.randint(1, stat1) + bonus1
    roll2 = rd.randint(1, stat2)
    if roll1 > 10*roll2:
        crit_count += 1
    elif roll1 > roll2:
        count += 1

print(count/n, crit_count/n)
