from pathlib import Path
import textwrap


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


class Computer:
    def __init__(self):
        self.registers = {"X": 1}
        self.instructions = []
        self.current_index = 0
        self.current_wait = 0
        self.cycle = 0

    def feed(self, instructions):
        self.instructions += instructions

    def run(self, draw_output=False):
        try:
            instruction = self.instructions[self.current_index]
        except IndexError:
            return
        result = self.registers["X"]
        if instruction.strip() == "noop":
            self.current_index += 1
            self.current_wait = 0
        else:
            if self.current_wait == 1:
                self.current_index += 1
                self.current_wait = 0
                param = int(instruction.split()[-1])
                self.registers["X"] += param
                # print(f"Cycle {self.cycle + 1}, adding {param} to {result} = {self.registers['X']}")
            else:
                self.current_wait += 1
        self.cycle += 1
        if not draw_output:
            return result
        if -1 <= (result % 40) - ((self.cycle - 1) % 40) <= 1:
            return "#"
        return "."

    def run_many(self, n):
        for _ in range(n):
            result = self.run()
        return result


def main_a(data):
    c = Computer()
    c.feed(data)
    result = 20 * c.run_many(20)
    for index in range(5):
        result += c.run_many(40) * (60 + index * 40)
    print(result)


def main_b(data):
    c = Computer()
    c.feed(data)
    screen = []
    while True:
        result = c.run(draw_output=True)
        if not result:
            break
        screen.append(result)

    for line in textwrap.wrap("".join(screen), 40):
        print(line)


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
