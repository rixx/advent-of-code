from pathlib import Path


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


def get_forest(data):
    result = []
    for line in data:
        row = []
        for number in line.strip():
            row.append({"visible": False, "height": int(number)})
        result.append(row)
    return result


def generate_sequences(forest):
    for line in forest:
        yield line
    for line in forest:
        yield reversed(line)
    for index in range(len(forest[0])):
        yield [line[index] for line in forest]
    for index in range(len(forest[0])):
        yield [line[index] for line in reversed(forest)]


def update_visibility(forest):
    for sequence in generate_sequences(forest):
        lowest_tree = -1
        for item in sequence:
            if item["height"] > lowest_tree:
                lowest_tree = item["height"]
                item["visible"] = True
    return forest


def count_visible(forest):
    return len([tree for line in forest for tree in line if tree["visible"]])


def main_a(data):
    forest = get_forest(data)
    forest = update_visibility(forest)
    print(count_visible(forest))


def generate_sequence(forest, x, y):
    yield forest[x][y + 1 :]
    yield forest[x][:y][::-1]
    column = [line[y] for line in forest]
    yield column[x + 1 :]
    yield column[:x][::-1]


def calculate_score(forest, x, y):
    total = 1
    own_height = forest[x][y]["height"]
    for sequence in generate_sequence(forest, x, y):
        if not sequence:
            return 0
        current_score = 0
        for entry in sequence:
            current_score += 1
            if entry["height"] >= own_height:
                break
        total *= current_score
    return total


def main_b(data):
    forest = get_forest(data)
    max_score = 0
    for x in range(len(forest)):
        for y in range(len(forest[0])):
            score = calculate_score(forest, x, y)
            if score > max_score:
                max_score = score
    print(max_score)


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
