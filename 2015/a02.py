""" Part 1 """

i = i.split("\n")

total = 0
for line in i:
    d = sorted([int(n) for n in line.split("x")])
    total += 2 * (d[0] * d[1] + d[0] * d[2] + d[1] * d[2]) + d[0] * d[1]

""" Part 2 """

total = 0
for line in i:
    d = sorted([int(n) for n in line.split("x")])
    total += 2 * (d[0] + d[1]) + d[0] * d[1] * d[2]
