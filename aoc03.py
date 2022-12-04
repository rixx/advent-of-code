from pathlib import Path
import string


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        for line in fp.readlines():
            length = len(line)
            yield (line[: length // 2], line[length // 2 :])


def get_backpack_score(comp_a, comp_b):
    common_letter = (set(comp_a) & set(comp_b)).pop()
    if common_letter in string.ascii_lowercase:
        return ord(common_letter) - 96
    return ord(common_letter) - 38


def main_a():
    data = parse_data()
    total = 0
    for backpack in data:
        total += get_backpack_score(*backpack)
    print(total)


def main_b():
    data = parse_data()


if __name__ == "__main__":
    main_a()
    # main_b()
