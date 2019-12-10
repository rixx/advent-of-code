from fractions import Fraction


def read_chart(string):
    nested = [list(line) for line in string.strip().split("\n")]
    return {
        (x, y): nested[x][y]
        for x in range(len(nested))
        for y in range(len(nested[0]))
    }, len(nested), len(nested[0])


def find_base(string):
    max_asteroids = 0
    max_position = None
    chart, rows, columns = read_chart(string)

    for row in range(rows):
        for column in range(columns):
            if chart[(row, column)] != '#':
                continue
            blocked_directions = set()
            seen_locations = set()
            checked_locations = set()
            print(f"Checking coordinate {row}, {column}")
            for distance in range(max(rows, columns)):
                for row_distance in range(-distance, distance + 1):
                    for column_distance in range(-distance, distance + 1):
                        check_row = row + row_distance
                        check_column = column + column_distance
                        if not (check_row, check_column) in chart:
                            continue
                        if (check_row, check_column) in checked_locations or (check_row == row and check_column == column):
                            continue
                        checked_locations.add((check_row, check_column))
                        if chart[(check_row, check_column)] != '#':
                            continue
                        print(f"  Checking if we can see {check_row}, {check_column}")
                        if row_distance == 0 or column_distance == 0:
                            reduced_row = 1 if row_distance else 0
                            reduced_column = 1 if column_distance else 0
                        else:
                            fraction = Fraction(row_distance, column_distance)
                            reduced_row = abs(fraction.numerator) * (-1 if row_distance < 0 else 1)
                            reduced_column = abs(fraction.denominator) * (-1 if column_distance < 0 else 1)
                        print(f"  Calculated reduced direction {reduced_row}, {reduced_column} from {row_distance, column_distance}")
                        if (reduced_row, reduced_column) in blocked_directions:
                            print("  This direction is blocked already")
                            continue
                        blocked_directions.add((reduced_row, reduced_column))
                        seen_locations.add((check_row, check_column))
                        print(f"  Seen new asteroid!")
            if len(seen_locations) > max_asteroids:
                max_asteroids = len(seen_locations)
                max_position = (row, column)
            print(f"{len(seen_locations)} at {row}, {column}")
    print(f"{max_asteroids} at {max_position}")
find_base("""#....#.....#...#.#.....#.#..#....#
#..#..##...#......#.....#..###.#.#
#......#.#.#.....##....#.#.....#..
..#.#...#.......#.##..#...........
.##..#...##......##.#.#...........
.....#.#..##...#..##.....#...#.##.
....#.##.##.#....###.#........####
..#....#..####........##.........#
..#...#......#.#..#..#.#.##......#
.............#.#....##.......#...#
.#.#..##.#.#.#.#.......#.....#....
.....##.###..#.....#.#..###.....##
.....#...#.#.#......#.#....##.....
##.#.....#...#....#...#..#....#.#.
..#.............###.#.##....#.#...
..##.#.........#.##.####.........#
##.#...###....#..#...###..##..#..#
.........#.#.....#........#.......
#.......#..#.#.#..##.....#.#.....#
..#....#....#.#.##......#..#.###..
......##.##.##...#...##.#...###...
.#.....#...#........#....#.###....
.#.#.#..#............#..........#.
..##.....#....#....##..#.#.......#
..##.....#.#......................
.#..#...#....#.#.....#.........#..
........#.............#.#.........
#...#.#......#.##....#...#.#.#...#
.#.....#.#.....#.....#.#.##......#
..##....#.....#.....#....#.##..#..
#..###.#.#....#......#...#........
..#......#..#....##...#.#.#...#..#
.#.##.#.#.....#..#..#........##...
....#...##.##.##......#..#..##....""")

#find_base("""
#......#.#.
##..#.#....
#..#######.
#.#.#.###..
#.#..#.....
#..#....#.#
##..#....#.
#.##.#..###
###...#..#.
#.#....####
#        """)
