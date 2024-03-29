import re
from pathlib import Path


def is_nice(s):
    vowels = r"[aeiou]"
    letters_twice = r"(\w)\1"
    naughty = ["ab", "cd", "pq", "xy"]

    if len(re.findall(vowels, s)) < 3:
        return False
    if not re.search(letters_twice, s):
        return False
    if any(n in s for n in naughty):
        return False
    return True


def is_nice_new(s):
    letters_twice = r"((\w{2})).*\1"
    letter_between = r"(.).\1"
    if not re.search(letters_twice, s):
        return False
    if not re.search(letter_between, s, flags=re.DOTALL):
        return False
    return True


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


def main_a():
    data = parse_data()
    nice = 0
    for line in data:
        if is_nice(line):
            nice += 1
    print(nice)


def main_b():
    data = parse_data()
    nice = 0
    assert is_nice_new("qjhvhtzxzqqjkmpb")
    assert is_nice_new("xxyxx")
    assert not is_nice_new("uurcxstgmygtbstg")
    assert not is_nice_new("ieodomkazucvgmuy")
    for line in data:
        if is_nice_new(line):
            nice += 1
    print(nice)


if __name__ == "__main__":
    # main_a()
    main_b()
