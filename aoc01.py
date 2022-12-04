def main_a():
    with open("aoc01.txt") as fp:
        text = fp.readlines()

    current_max = 0
    current_count = 0

    for line in text:
        line = line.strip()
        if not line:
            if current_count > current_max:
                current_max = current_count
            current_count = 0
        else:
            current_count += int(line)
    print(current_max)


def main_b():
    with open("aoc01.txt") as fp:
        text = fp.readlines()

    current_top = [0, 0, 0]
    all_counts = []
    current_count = 0

    for line in text:
        line = line.strip()
        if line:
            current_count += int(line)
        else:
            all_counts.append(current_count)
            current_count = 0
    print(sum(sorted(all_counts, reverse=True)[:3]))


if __name__ == "__main__":
    main_b()
