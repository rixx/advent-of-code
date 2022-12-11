from copy import deepcopy
from pathlib import Path
import sys

MAX_WORRY = 11 * 7 * 13 * 5 * 3 * 17 * 2 * 19


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.read()
    return data.split("\n\n")


class Monkey:
    def __init__(self, instructions, part_1=True):
        name, starting, operation, test, true, false = instructions.strip().split("\n")
        self.name = name.split()[-1].strip(":")
        self.items = [int(item) for item in starting.split(":")[-1].split(",")]
        self.operation = operation.split("=")[-1].strip()
        self.test_divisible = int(test.split()[-1])
        self.output_true = int(true.split()[-1])
        self.output_false = int(false.split()[-1])
        self.inspection_counter = 0
        self.part_1 = part_1

    def inspect(self):
        self.inspection_counter += 1
        worry = self.items.pop(0)
        left, operator, right = self.operation.replace("old", str(worry)).split()
        if operator == "+":
            worry = int(left) + int(right)
        elif operator == "*":
            worry = int(left) * int(right)
        if self.part_1:
            worry = int(int(worry) / 3)
        worry = worry % MAX_WORRY
        return {
            "item": worry,
            "move_to": self.output_true
            if worry % self.test_divisible == 0
            else self.output_false,
        }

    def run_round(self):
        result = []
        while self.items:
            result.append(self.inspect())
        return result

    def add_item(self, item: int):
        self.items.append(item)


def run_round(monkeys):
    for monkey in monkeys.values():
        result = monkey.run_round()
        for r in result:
            monkeys[r["move_to"]].add_item(r["item"])
    return monkeys


def get_result(monkeys):
    monkey_list = sorted(
        monkeys.values(), key=lambda m: m.inspection_counter, reverse=True
    )
    print(monkey_list[0].inspection_counter * monkey_list[1].inspection_counter)


def main_a(data):
    monkey_list = [Monkey(instructions) for instructions in data]
    monkeys = {int(monkey.name): monkey for monkey in monkey_list}
    for _ in range(20):
        monkeys = run_round(monkeys)
    for monkey in monkeys.values():
        print(
            f"Monkey {monkey.name} inspected items {monkey.inspection_counter} times."
        )
    get_result(monkeys)


def main_b(data):
    monkey_list = [Monkey(instructions, part_1=False) for instructions in data]
    monkeys = {int(monkey.name): monkey for monkey in monkey_list}
    for _ in range(10_000):
        monkeys = run_round(monkeys)
    for monkey in monkeys.values():
        print(
            f"Monkey {monkey.name} inspected items {monkey.inspection_counter} times."
        )
    get_result(monkeys)


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
