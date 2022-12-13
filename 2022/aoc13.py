import copy
import json
from functools import cmp_to_key
from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.read().split("\n\n")
    result = []
    for pair in data:
        first, second = pair.strip().split("\n")
        result.append((json.loads(first), json.loads(second)))
    return result


def parse_data_2():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    result = []
    for line in data:
        if not line.strip():
            continue
        result.append(json.loads(line))
    return result


def has_correct_order(left, right):
    left = copy.deepcopy(left)
    right = copy.deepcopy(right)
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        return None
    if isinstance(left, int) and isinstance(right, list):
        return has_correct_order([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return has_correct_order(left, [right])
    # Finally, if both are lists, we compare the lists
    if not left and not right:
        return None
    if right and not left:
        return True
    if left and not right:
        return False
    left_head = left.pop(0)
    right_head = right.pop(0)
    comp_result = has_correct_order(left_head, right_head)
    if comp_result is not None:
        return comp_result
    return has_correct_order(left, right)


def main_a(data):
    result = 0
    for index, pair in enumerate(data):
        if has_correct_order(*pair):
            result += index + 1
    print(result)


def cmp_order(left, right):
    if has_correct_order(left, right):
        return -1
    return 1


def main_b(data):
    div_0 = [[2]]
    div_1 = [[6]]
    data += [div_0, div_1]
    result = sorted(data, key=cmp_to_key(cmp_order))
    key = (result.index(div_0) + 1) * (result.index(div_1) + 1)
    print(key)


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    data = parse_data_2()
    print("\n##### Part 2 #####")
    main_b(data)
