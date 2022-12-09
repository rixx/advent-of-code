from pathlib import Path


def parse_data():
    result = {}
    with open(Path(__file__).stem + ".txt") as fp:
        for line in fp.readlines():
            left, right = line.split("->")
            result[right.strip()] = left.strip()
    return result


def evaluate(variable, lookup):
    if isinstance(variable, int) or variable.isnumeric():
        return int(variable)
    equation = lookup[variable]
    result = None
    if isinstance(equation, int) or equation.isnumeric():
        result = int(equation)
    elif not " " in equation:
        result = evaluate(equation, lookup)
    elif equation.startswith("NOT"):
        result = ~evaluate(equation.split()[-1], lookup)
    else:
        left, operator, right = equation.split()
        left = evaluate(left, lookup)
        right = evaluate(right, lookup)
        if operator == "AND":
            result = left & right
        elif operator == "OR":
            result = left | right
        elif operator == "LSHIFT":
            result = left << right
        elif operator == "RSHIFT":
            result = left >> right
    lookup[variable] = result
    return result


def main_a(data):
    print(evaluate("a", data))


def main_b(data):
    data["b"] = "3176"
    print(evaluate("a", data))


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    data = parse_data()
    print("\n##### Part 2 #####")
    main_b(data)
