from pathlib import Path
from collections import defaultdict
import more_itertools

AIR = 0
ROCK = 1
SAND = 2
PRINT_MAP = {
    AIR: ".",
    ROCK: "#",
    SAND: "o",
}
START = (500, 0)


def to_coords(s):
    s = s.split(",")
    return int(s[0]), int(s[1])


def get_coordinates(first, second):
    x1, y1 = to_coords(first)
    x2, y2 = to_coords(second)
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            yield x1, y
    elif y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            yield x, y1
    else:
        raise Exception("aah")


def parse_data():
    result = defaultdict(int)
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    for line in data:
        for pair in more_itertools.pairwise(line.split("->")):
            for coordinates in get_coordinates(*pair):
                result[coordinates] = ROCK
    return result


class Field:
    def __init__(self, data, bottom_offset=0):
        self.field = data
        self.sand_generated = 0
        self.largest_y = self.get_largest_y()
        self.cutoff = None
        if bottom_offset:
            self.cutoff = self.largest_y + bottom_offset - 1

    def get_largest_y(self):
        values = {y for x, y in self.field.keys()}
        return max(values)

    @property
    def sand_count(self):
        return len([v for v in self.field.values() if v == SAND])

    def is_free(self, x, y):
        if self.cutoff and y == self.cutoff:
            return False
        return self.field[x, y] == AIR

    def generate_sand(self):
        x, y = START
        if not self.is_free(x, y):
            return False
        while True:
            if self.is_free(x, y + 1):
                y += 1
                if y > self.largest_y and not self.cutoff:
                    return False
            elif self.is_free(x - 1, y + 1):
                x -= 1
                y += 1
            elif self.is_free(x + 1, y + 1):
                x += 1
                y += 1
            else:
                self.field[(x, y)] = SAND
                self.sand_generated += 1
                return True

    def print(self):
        y_values = {y for x, y in self.field.keys()}
        x_values = {x for x, y in self.field.keys()}
        x_range = min(x_values) - 1, max(x_values) + 3
        y_range = 0, max(y_values) + 1
        for y in range(*y_range):
            line = ""
            for x in range(*x_range):
                line += PRINT_MAP[self.field[x, y]]
            print(line)

    def run_to_completion(self):
        while True:
            if not self.generate_sand():
                return self.sand_count


def main_a(data):
    field = Field(data)
    print(field.run_to_completion())


def main_b(data):
    field = Field(data, bottom_offset=2)
    print(field.run_to_completion())


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
