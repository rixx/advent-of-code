from pathlib import Path
from collections import defaultdict, Counter

from tqdm import tqdm


UNKNOWN = 0
KNONW_EMPTY = 1
BEACON = 2
SENSOR = 3

SYMBOLS = {
    UNKNOWN: ".",
    KNONW_EMPTY: "#",
    BEACON: "B",
    SENSOR: "S",
}


def get_coords(s):
    left, right = s[s.find("x=") :].split(", ")
    return int(left.strip("x=")), int(right.strip("y="))


def parse_data():
    result = []
    with open(Path(__file__).stem + ".txt") as fp:
        for line in fp.readlines():
            left, right = line.split(":")
            result.append((get_coords(left), get_coords(right)))
    return result


def get_locations(sensor, beacon, row=None):
    distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    ydist = abs(sensor[1] - row)
    if ydist > distance:
        return

    for x in range(distance - ydist + 1):
        if x + ydist > distance:
            continue
        yield sensor[0] + x, row
        yield sensor[0] + x, row
        yield sensor[0] - x, row
        yield sensor[0] - x, row


class Map:
    def __init__(self, beacons, row=None):
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
        self.row = row
        self.map = defaultdict(int)
        self.known_empty = []
        for sensor, beacon in tqdm(beacons):
            self.add_beacon(sensor, beacon)

    def add_beacon(self, sensor, beacon):
        self.map[sensor] = SENSOR
        self.map[beacon] = BEACON
        self.update_range(*sensor)
        self.update_range(*beacon)
        for location in get_locations(sensor, beacon, row=self.row):
            if self.map[location] == UNKNOWN:
                self.map[location] = KNONW_EMPTY
                self.known_empty.append(location)

    def update_range(self, x, y):
        if x > self.max_x:
            self.max_x = x
        if y > self.max_y:
            self.max_y = y
        if x < self.min_x:
            self.min_x = x
        if y < self.min_y:
            self.min_y = y

    def count_row(self):
        return len(self.known_empty)

    def print(self):
        for y in range(self.min_y, self.max_y + 1):
            line = f"{y + 1} "
            for x in range(self.min_x, self.max_x + 1):
                line += SYMBOLS[self.map[(x, y)]]
            print(line)


def main_a(data):
    chart = Map(data, row=2000000)
    print(chart.count_row())


def main_b(data):
    search = 4000000
    # search = 20
    counter = Counter()
    for sensor, beacon in data:
        distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        outside = distance + 1
        for x in tqdm(range(outside + 1)):
            y = outside - x  # WARNING off by one
            for coords in [
                (sensor[0] + x, sensor[1] - y),
                (sensor[0] + x, sensor[1] + y),
                (sensor[0] - x, sensor[1] - y),
                (sensor[0] - x, sensor[1] + y),
            ]:
                if (0 <= coords[0] <= search) and (0 <= coords[1] <= search):
                    counter.update([coords])
        print(len(counter.keys()))
    result, _ = counter.most_common(1)[0]
    print(result)
    print(result[0] * 4000000 + result[1])


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    # main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
