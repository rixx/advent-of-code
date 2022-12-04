from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    for line in data:
        left, right = line.split(",")
        left = left.split("-")
        right = right.split("-")
        yield ((int(left[0]), int(left[1])), (int(right[0]), int(right[1])))


def check_full_overlap(left, right):
    if left[0] <= right[0] and left[1] >= right[1]:
        return True
    left, right = right, left
    if left[0] <= right[0] and left[1] >= right[1]:
        return True


def check_partial_overlap(left, right):
    overlaps = (
        (left[0], right[0], left[1]),
        (left[0], right[1], left[1]),
        (right[0], left[0], right[1]),
        (right[0], left[1], right[1]),
    )
    for l, m, r in overlaps:
        if l <= m <= r:
            return True


def main_a():
    count = 0
    for left, right in parse_data():
        if check_full_overlap(right, left):
            count += 1
    print(count)


def main_b():
    count = 0
    for left, right in parse_data():
        if check_partial_overlap(left, right):
            count += 1
    print(count)


if __name__ == "__main__":
    # main_a()
    main_b()
