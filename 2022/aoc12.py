import string
from contextlib import suppress
from pathlib import Path

START = "S"
END = "E"

MAP = {letter: index + 1 for index, letter in enumerate(string.ascii_lowercase)}
MAP[START] = 0
MAP[END] = 27


def parse_data(start_cutoff=0):
    result = []
    start_coords = []
    end_coords = None
    with open(Path(__file__).stem + ".txt") as fp:
        for x_coord, line in enumerate(fp.readlines()):
            line_result = [MAP[letter] for letter in line.strip()]
            with suppress(ValueError):
                for index in range(len(line_result)):
                    if line_result[index] <= start_cutoff:
                        start_coords.append((x_coord, index))
            with suppress(ValueError):
                end_coords = (x_coord, line_result.index(27))
            result.append(line_result)
    grid = {}
    for x in range(len(result)):
        for y in range(len(result[0])):
            distances = {}
            value = result[x][y]
            for x2, y2 in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                with suppress(IndexError):
                    if x2 < 0 or y2 < 0:
                        continue
                    if result[x2][y2] - value <= 1:
                        distances[(x2, y2)] = 1
            grid[(x, y)] = distances

    return grid, start_coords, end_coords


def find_way(grid, start, end):
    nodes = grid.keys()
    unvisited_nodes = list(grid.keys())
    # unvisited = {node: None for node in nodes}
    shortest_path = {node: 9999999999 for node in nodes}
    shortest_path[start] = 0
    previous_nodes = {start: None}
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if not current_min_node:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        for neighbor, distance in grid[current_min_node].items():
            tentative_value = shortest_path[current_min_node] + distance
            if (
                shortest_path[neighbor] is None
                or tentative_value < shortest_path[neighbor]
            ):
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node
        unvisited_nodes.remove(current_min_node)
    return shortest_path, previous_nodes


def main_a(grid, start, end):
    start = start[0]
    path, nodes = find_way(grid, start, end)
    print(path[end])


def main_b(grid, starts, end):
    min_result = 99999999
    print(f"Found {len(starts)} starts")
    for index, start in enumerate(starts):
        path, nodes = find_way(grid, start, end)
        way = path[end]
        if way < min_result:
            min_result = way
        if index % 10 == 0:
            print(f"Run {index}, result {min_result}")
    print(min_result)


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(*data)
    data = parse_data(start_cutoff=1)
    print("\n##### Part 2 #####")
    main_b(*data)
