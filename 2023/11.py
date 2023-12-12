from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        map = [ [ col for col in row ] for row in input.strip().split('\n') ]
        galaxy_coords = get_galaxy_coordinates(map)
        expanded_coords = expand_universe(map, galaxy_coords, 2)
        return get_all_distances(expanded_coords)

    def test_input_one(self):
        return """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    def solve_part_two(self, input):
        map = [ [ col for col in row ] for row in input.strip().split('\n') ]
        galaxy_coords = get_galaxy_coordinates(map)
        expanded_coords = expand_universe(map, galaxy_coords, 1000000)
        return get_all_distances(expanded_coords)

def get_galaxy_coordinates(map):
    galaxies = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                galaxies.append((y, x))

    return galaxies

def expand_universe(map, galaxy_coords, expansion__factor):
    rows = len(map)
    cols = len(map[0])

    y_exists = [ False for _ in range(rows) ]
    x_exists = [ False for _ in range(cols) ]

    for y, x in galaxy_coords:
        y_exists[y] = True
        x_exists[x] = True

    new_y_values = list(range(rows))
    for i in range(rows):
        if not y_exists[i]:
            for j in range(i + 1, rows):
                new_y_values[j] += expansion__factor - 1

    new_x_values = list(range(cols))
    for i in range(0, cols):
        if not x_exists[i]:
            for j in range(i + 1, cols):
                new_x_values[j] += expansion__factor - 1

    new_coords = []
    for y, x in galaxy_coords:
        new_coords.append((new_y_values[y], new_x_values[x]))

    return new_coords

def distance_between(coords_1, coords_2):
    y_1, x_1 = coords_1
    y_2, x_2 = coords_2

    return abs(y_1 - y_2) + abs(x_1 - x_2)

def get_all_distances(coords):
    total = 0
    num_coords = len(coords)
    for i in range(num_coords):
        for j in range(i, num_coords):
            total += distance_between(coords[i], coords[j])

    return total

thing = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""