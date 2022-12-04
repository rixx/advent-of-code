from collections import defaultdict
from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.read()
    return data


def main_a():
    data = parse_data()
    x = 0
    y = 0
    chart = defaultdict(int)
    chart[(x, y)] += 1
    for direction in data:
        if direction == "^":
            y += 1
        elif direction == "v":
            y -= 1
        elif direction == "<":
            x -= 1
        elif direction == ">":
            x += 1
        else:
            continue
        chart[(x, y)] += 1
    print(len(chart.keys()))


def main_b():
    data = parse_data()


if __name__ == "__main__":
    main_a()
    # main_b()
