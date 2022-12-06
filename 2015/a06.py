from pathlib import Path
from collections import defaultdict


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


class Grid:
    def __init__(self):
        self.grid = defaultdict(int)

    def run(self, instruction, v2=False):
        instruction = instruction.split()
        coordinates = self.get_range(instruction[-3], instruction[-1])
        if not v2:
            value = None
            toggle = instruction[0] == "toggle"
            if not toggle:
                value = int(instruction[1] == "on")
            self.set_range(coordinates, value, toggle)
        else:
            if instruction[0] == "toggle":
                value = 2
            elif instruction[1] == "on":
                value = 1
            else:
                value = -1
            self.inc_range(coordinates, value)

    def get_range(self, start, end):
        start_x, start_y = start.split(",")
        end_x, end_y = end.split(",")
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                yield (x, y)

    def set_range(self, iterator, value=None, toggle=False):
        for coordinates in iterator:
            if toggle:
                value = int(not self.grid.get(coordinates))
            self.grid[coordinates] = value

    def inc_range(self, iterator, value):
        for coordinates in iterator:
            self.grid[coordinates] += value
            if self.grid[coordinates] < 0:
                self.grid[coordinates] = 0


def main_a(data):
    grid = Grid()
    for line in data:
        grid.run(line)
    print(sum(grid.grid.values()))


def main_b(data):
    grid = Grid()
    for line in data:
        grid.run(line, v2=True)
    print(sum(grid.grid.values()))


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    # main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
