from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        map = [ [ col for col in row ] for row in input.strip().split('\n') ]
        tilt(map, 'N')

        return weigh(map)

    def test_input_one(self):
        return """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

    def solve_part_two(self, input):
        map = [ [ col for col in row ] for row in input.strip().split('\n') ]
        spin_cycle = ['N', 'W', 'S', 'E']
        cycles = 1000000000
        i = 0
        map_memory = {}

        while i < cycles:
            map_key = ''.join([ ''.join(row) for row in map ])
            if map_key in map_memory:
                first_occurrence = map_memory[map_key]
                cycles_remaining = (cycles - first_occurrence) % (i - first_occurrence)
                # Fast forward like a billion cycles, that is NOT an exaggeration
                i = cycles - cycles_remaining
                map_memory.clear()

            for direction in spin_cycle:
                tilt(map, direction)

            map_memory[map_key] = i
            i += 1

        return weigh(map)

def tilt(map, direction):
    d_i = direction_new[direction]
    axis_1_length = len(map) if direction == 'N' or direction == 'S' else len(map[0])

    # if we're tilting to the front, start from the front
    axis_1_range = range(axis_1_length) if d_i == -1 else range(axis_1_length - 1, -1, -1)

    for i in axis_1_range:
        line = get_line(map, i, direction)
        new_line = tilt_line(line)
        replace_line(map, i, direction, new_line)

def get_line(map, i, direction):
    line = [ map[y][i] for y in range(len(map)) ] if direction == 'N' or direction == 'S' else map[i]
    corrected_line = line if direction_new[direction] == -1 else list(reversed(line))
    return ''.join(corrected_line)

def replace_line(map, i, direction, new_line):
    corrected_line = new_line if direction_new[direction] == -1 else list(reversed(new_line))
    if direction == 'N' or direction == 'S':
        for j in range(len(corrected_line)):
            map[j][i] = corrected_line[j]
    else:
        map[i] = list(corrected_line)


line_memory = {}
def memoize_tilt_line(f):
    def inner(line):
        if line not in line_memory:
            line_memory[line] = f(line)
        return line_memory[line]
    return inner

@memoize_tilt_line
def tilt_line(line):
    new_line = list(line)
    for i in range(len(new_line)):
        if new_line[i] != 'O':
            continue

        resting_i = i
        current_i = i - 1

        while 0 <= current_i < len(new_line) and new_line[current_i] == '.':
            resting_i = current_i
            current_i -= 1

        if resting_i != i:
            new_line[resting_i] = new_line[i]
            new_line[i] = '.'

    return ''.join(new_line)


def weigh(map):
    total = 0
    for i in range(len(map)):
        weight = len(map) - i
        total += weight * map[i].count('O')
    return total

direction_coords = {
    'N': (-1, 0),
    'W': (0, -1),
    'S': (1, 0),
    'E': (0, 1),
}

direction_new = {
    'N': -1,
    'W': -1,
    'S': 1,
    'E': 1,
}