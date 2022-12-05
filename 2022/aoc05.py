from collections import defaultdict
from pathlib import Path


class Stack:
    """Index 0 has the bottom of the pile."""

    def __init__(self, items):
        self.stack = list(reversed([i for i in items if i.strip()]))

    def remove(self, n, model=9000):
        result = []
        if model == 9000:
            for _ in range(n):
                result.append(self.stack.pop(-1))
        elif model == 9001:
            result = self.stack[-n:]
            self.stack = self.stack[:-n]
        return result

    def add(self, stack):
        self.stack += stack

    def __repr__(self):
        return f"Stack({''.join(self.stack)})"


def parse_data():
    stacks = []
    moves = []
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()

    stack_strings = []
    is_move = False
    for line in data:
        if line.strip().startswith("1"):
            continue
        if not line.strip():
            is_move = True
        elif not is_move:
            stack_strings.append(line)
        else:
            moves.append(line)

    for index in range(9):
        string_index = 1 + 4 * index
        stacks.append(
            Stack(
                [
                    content[string_index] if len(content) > string_index else None
                    for content in stack_strings
                ]
            )
        )
    return stacks, moves


def main_a():
    stacks, moves = parse_data()
    for move in moves:
        move = move.split(" ")
        stacks[int(move[5]) - 1].add(stacks[int(move[3]) - 1].remove(int(move[1])))
    for stack in stacks:
        print(stack.stack[-1], end="")


def main_b():
    stacks, moves = parse_data()
    for move in moves:
        move = move.split(" ")
        stacks[int(move[5]) - 1].add(
            stacks[int(move[3]) - 1].remove(int(move[1]), model=9001)
        )
    for stack in stacks:
        print(stack.stack[-1], end="")


if __name__ == "__main__":
    # main_a()
    main_b()
