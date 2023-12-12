from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        tiles = [ line for line in input.split('\n') ]

        y, x, dir = get_start_tile(tiles)
        steps = 1
        while True:
            y, x, dir = get_next_coordinates(tiles, y, x, dir)
            steps += 1

            if tiles[y][x] == 'S':
                break

        return int(steps / 2)

    def test_input_one(self):
        return """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

    def solve_part_two(self, input):
        tiles = [ line for line in input.strip().split('\n') ]
        pipe_map = [ [ '.' for _ in range(len(tiles[0])) ] for _ in range(len(tiles)) ]

        start_y, start_x, start_dir = get_start_tile(tiles)
        y, x, dir = start_y, start_x, start_dir
        pipe_map[y][x] = tiles[y][x]

        while True:
            y, x, dir = get_next_coordinates(tiles, y, x, dir)
            pipe_map[y][x] = tiles[y][x]

            if tiles[y][x] == 'S':
                break

        # Do it again, but replace dots
        y, x, dir = start_y, start_x, start_dir
        while True:
            y, x, dir = get_next_coordinates(pipe_map, y, x, dir, True)
            if pipe_map[y][x] == 'S':
                break

        [ print(''.join(row)) for row in pipe_map ]

        # Now count them
        outside_dots = 0
        inside_dots = 0
        for row in pipe_map:
            for tile in row:
                if tile == 'O':
                    outside_dots += 1
                elif tile == 'I':
                    inside_dots += 1

        return ('O', outside_dots), ('I', inside_dots)

    def test_input_two(self):
        return """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


def get_start_tile(tiles):
    start_y = None
    start_x = None

    rows = len(tiles)
    cols = len(tiles[0])

    for y in range(rows):
        for x in range(cols):
            if tiles[y][x] == 'S':
                start_x = x
                break

        if start_x is not None:
            start_y = y
            break

    directions = [
        (-1, 0, 'N'),
        (0, 1, 'E'),
        (1, 0, 'S'),
        (0, -1, 'W'),
    ]
    is_in_bounds = lambda c: (
        (0 <= start_y + c[0] <= rows) and
        (0 <= start_x + c[1] <= cols)
    )

    possible_directions = filter(is_in_bounds, directions)
    for y_d, x_d, toward in possible_directions:
        next_y = start_y + y_d
        next_x = start_x + x_d

        next_tile = tiles[next_y][next_x]

        if connectors[opposite_dir[toward]][next_tile]:
            # Take the first one and don't look back
            return start_y, start_x, toward

def get_next_coordinates(tiles, y, x, current_dir, replace_dots=False):
    next_y, next_x = y, x

    if current_dir == 'W':
        next_x -= 1
    elif current_dir == 'E':
        next_x += 1
    elif current_dir == 'N':
        next_y -= 1
    elif current_dir == 'S':
        next_y += 1

    if replace_dots:
        replace_dots_to_sides(tiles, next_y, next_x, current_dir)

    next_dir = get_next_direction(tiles, next_y, next_x, current_dir)

    if replace_dots:
        replace_dots_to_sides(tiles, next_y, next_x, next_dir)

    return (next_y, next_x, next_dir)

def get_next_direction(tiles, y, x, current_dir):
    tile = tiles[y][x]
    for connects_toward in connectors:
        # Try to find a corner first

        if opposite_dir[connects_toward] != current_dir:
            if connectors[connects_toward][tile]:
                return connects_toward

    # We are going in a straight line
    return current_dir

def replace_dots_to_sides(tiles, y, x, current_dir):
    # assume these are outside
    replace_dots_in_direction(tiles, y, x, left_90_deg[current_dir], 'O')

    # assume these are inside
    replace_dots_in_direction(tiles, y, x, right_90_deg[current_dir], 'I')

def replace_dots_in_direction(tiles, y, x, dir_coords, replacement):
    rows = len(tiles)
    cols = len(tiles[0])

    queue = []
    y_d, x_d = dir_coords
    queue.append((y + y_d, x + x_d))

    while len(queue):
        y, x = queue.pop(0)
        if 0 <= y < rows and 0 <= x < cols and tiles[y][x] == '.':
            tiles[y][x] = replacement
            for y_d, x_d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                queue.append((y + y_d, x + x_d))


opposite_dir = {
    'E': 'W',
    'W': 'E',
    'N': 'S',
    'S': 'N',
}

connects_west = {
    'F': False,
    '-': True,
    '7': True,
    '|': False,
    'J': True,
    'L': False,
    '.': False,
    'S': True,
}

connects_east = {
    'F': True,
    '-': True,
    '7': False,
    '|': False,
    'J': False,
    'L': True,
    '.': False,
    'S': True,
}

connects_north = {
    'F': False,
    '-': False,
    '7': False,
    '|': True,
    'J': True,
    'L': True,
    '.': False,
    'S': True,
}

connects_south = {
    'F': True,
    '-': False,
    '7': True,
    '|': True,
    'J': False,
    'L': False,
    '.': False,
    'S': True,
}

connectors = {
    'N': connects_north,
    'E': connects_east,
    'S': connects_south,
    'W': connects_west,
}

left_90_deg = {
    'N': (0, -1),
    'E': (-1, 0),
    'S': (0, 1),
    'W': (1, 0),
}

right_90_deg = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}