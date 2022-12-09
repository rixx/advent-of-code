from pathlib import Path


class Obj:
    def __init__(self, x, y):
        self.position = (x, y)

    def move(self, offset_x, offset_y):
        self.position = (self.position[0] + offset_x, self.position[1] + offset_y)

    def is_adjacent(self, other):
        return (
            max(
                abs(self.position[0] - other.position[0]),
                abs(self.position[1] - other.position[1]),
            )
            <= 1
        )

    def get_direction(self, own, other):
        if own == other:
            return 0
        if own < other:
            return 1
        return -1

    def move_towards(self, other):
        if self.is_adjacent(other):
            return
        self.move(
            self.get_direction(self.position[0], other.position[0]),
            self.get_direction(self.position[1], other.position[1]),
        )


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


MOVES = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def main_a(data):
    head = Obj(0, 0)
    tail = Obj(0, 0)
    known_positions = set()
    for line in data:
        direction, amount = line.strip().split()
        move = MOVES[direction]
        for _ in range(int(amount)):
            head.move(*move)
            tail.move_towards(head)
            known_positions.add(tail.position)
    print(len(known_positions))


def main_b(data):
    head = Obj(0, 0)
    tail = [Obj(0, 0) for _ in range(9)]
    known_positions = set()
    for line in data:
        direction, amount = line.strip().split()
        move = MOVES[direction]
        for _ in range(int(amount)):
            head.move(*move)
            tail[0].move_towards(head)
            for index in range(8):
                tail[index + 1].move_towards(tail[index])
            known_positions.add(tail[-1].position)
    print(len(known_positions))


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
