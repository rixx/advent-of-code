import more_itertools
import string
from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        for line in fp.readlines():
            length = len(line)
            yield (line[: length // 2], line[length // 2 :])


def parse_data_b():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return more_itertools.grouper(data, 3)


def get_backpack_score(comp_a, comp_b, comp_c=None):
    common_letter = set(comp_a) & set(comp_b)
    if comp_c:
        common_letter &= set(comp_c)
    common_letter = common_letter.pop()
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
    groups = parse_data_b()
    total = 0
    for group in groups:
        total += get_backpack_score(*group)
    print(total)


if __name__ == "__main__":
    # main_a()
    main_b()
