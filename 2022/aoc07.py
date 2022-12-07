from pathlib import Path


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.files = {}
        self.subdirectories = {}
        self.parent = parent

    def add_file(self, name, size):
        self.files[name] = size

    def add_subdirectory(self, name, subdir):
        self.subdirectories[name] = subdir

    def traverse(self):
        for subdir in self.subdirectories.values():
            for subsub in subdir.traverse():
                yield subsub
        yield self

    @property
    def size(self):
        return sum(self.files.values()) + sum(
            subdir.size for subdir in self.subdirectories.values()
        )


def parse_data():
    with open(Path(__file__).stem + ".txt") as fp:
        data = fp.readlines()
    return data


def parse_subtree(lines, current_index, parent=None):
    if not lines[current_index].startswith("$ cd"):
        raise Exception

    current_dir = Directory(lines[current_index].split()[-1], parent=parent)
    current_index += 2  # the next op is always an ls

    while True:
        try:
            line = lines[current_index].split()
        except IndexError:
            return current_dir, current_index
        if line[0] == "$":
            break
        current_index += 1
        if line[0] == "dir":
            continue
        current_dir.add_file(line[1], int(line[0]))

    # next we go somewhere
    while True:
        try:
            line = lines[current_index].split()
        except IndexError:
            return current_dir, current_index
        if not line[1] == "cd":
            raise Exception
        if line[2] == "..":
            return current_dir, current_index + 1
        subdir, current_index = parse_subtree(lines, current_index, parent=current_dir)
        current_dir.add_subdirectory(line[2], subdir)


def build_file_tree(data):
    return parse_subtree(data, 0)


def main_a(data):
    tree, _ = build_file_tree(data)
    result = []
    for directory in tree.traverse():
        size = directory.size
        if size <= 100000:
            result.append(size)
    print(sum(result))


def main_b(data):
    tree, _ = build_file_tree(data)
    total_size = tree.size
    min_size = tree.size - (70000000 - 30000000)
    result = 1000000000
    for directory in tree.traverse():
        size = directory.size
        if size >= min_size and size < result:
            result = size
    print(result)


if __name__ == "__main__":
    data = parse_data()
    print("##### Part 1 #####")
    main_a(data)
    print("\n##### Part 2 #####")
    main_b(data)
