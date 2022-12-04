from collections import defaultdict
from more_itertools import grouper
from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.read()
    return data


def get_direction(direction):
    x = 0
    y = 0
    if direction == "^":
        y += 1
    elif direction == "v":
        y -= 1
    elif direction == "<":
        x -= 1
    elif direction == ">":
        x += 1
    return x, y


def main_a():
    data = parse_data()
    x = 0
    y = 0
    chart = defaultdict(int)
    chart[(x, y)] += 1
    for direction in data:
        direction = get_direction(direction)
        x += direction[0]
        y += direction[1]
        chart[(x, y)] += 1
    print(len(chart.keys()))


def main_b():
    data = parse_data()
    santa = [0, 0]
    robo = [0, 0]
    chart = defaultdict(int)
    chart[tuple(santa)] += 2
    for s, r in grouper(data, 2):
        direction = get_direction(s)
        santa[0] += direction[0]
        santa[1] += direction[1]
        chart[tuple(santa)] += 1
        direction = get_direction(r)
        robo[0] += direction[0]
        robo[1] += direction[1]
        chart[tuple(robo)] += 1
    print(len(chart.keys()))


if __name__ == "__main__":
    # main_a()
    main_b()
