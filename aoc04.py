from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    for line in data:
        left, right = line.split(",")
        left = left.split("-")
        right = right.split("-")
        yield ((int(left[0]), int(left[1])), (int(right[0]), int(right[1])))


def check_overlap(left, right):
    if left[0] <= right[0] and left[1] >= right[1]:
        return True
    left, right = right, left
    if left[0] <= right[0] and left[1] >= right[1]:
        return True


def main_a():
    data = parse_data()
    count = 0
    for left, right in parse_data():
        if check_overlap(left, right) or check_overlap(right, left):
            count += 1
    print(count)


def main_b():
    data = parse_data()


if __name__ == "__main__":
    main_a()
    # main_b()
