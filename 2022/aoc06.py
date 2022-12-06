from pathlib import Path


def find_start(s, offset=4):
    for index in range(len(s) - 3):
        if len(set(s[index : index + offset])) == offset:
            return index + offset


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.read()
    return data


def main_a():
    data = parse_data()
    start = find_start("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    print(start)
    start = find_start(data)
    print(start)


def main_b():
    data = parse_data()


if __name__ == "__main__":
    main_a()
    # main_b()
