from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


def main_a():
    data = parse_data()


def main_b():
    data = parse_data()


if __name__ == "__main__":
    print("##### Part 1 #####")
    main_a()
    print("\n##### Part 2 #####")
    main_b()
