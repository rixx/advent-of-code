""" Part 1 """
i.count("(") - i.count(")")

""" Part 2 """
floor = 0
for position, direction in enumerate(i):
    floor += 1 if direction == "(" else -1
    if floor == -1:
        break
