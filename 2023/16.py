from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        grid = [ [ col for col in row ] for row in input.strip().split('\n') ]
        return find_energized_tiles(grid, 0, 0, 'E')

    def test_input_one(self):
        return r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

    def solve_part_two(self, input):
        grid = [ [ col for col in row ] for row in input.strip().split('\n') ]

        current_max = 0
        for y in range(len(grid)):
            energized_tiles = find_energized_tiles(grid, y, 0, 'E')
            current_max = max(current_max, energized_tiles)

            energized_tiles = find_energized_tiles(grid, y, len(grid[y]) - 1, 'W')
            current_max = max(current_max, energized_tiles)

        for x in range(len(grid[0])):
            energized_tiles = find_energized_tiles(grid, 0, x, 'S')
            current_max = max(current_max, energized_tiles)

            energized_tiles = find_energized_tiles(grid, len(grid) - 1, x, 'N')
            current_max = max(current_max, energized_tiles)

        return current_max


def find_energized_tiles(grid, y, x, current_direction):
    energized_tiles_with_dir = set()
    queue = [(y, x, current_direction)]

    while len(queue):
        y, x, current_direction = queue.pop()

        if not (0 <= y < len(grid) and 0 <= x < len(grid[y])):
            continue

        if (y, x, current_direction) in energized_tiles_with_dir:
            continue

        energized_tiles_with_dir.add((y, x, current_direction))

        current_tile = grid[y][x]
        next_directions = tile_directions[current_tile][current_direction]
        for next_direction in next_directions:
            d_y, d_x = direction_coords[next_direction]
            queue.append((y + d_y, x + d_x, next_direction))

    return len(set([ (y, x) for y, x, _ in energized_tiles_with_dir ]))


direction_coords = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}

tile_directions = {
    '.':  {
        'N': ['N'],
        'E': ['E'],
        'S': ['S'],
        'W': ['W'],
    },
    '/': {
        'N': ['E'],
        'E': ['N'],
        'S': ['W'],
        'W': ['S'],
    },
    '\\': {
        'N': ['W'],
        'E': ['S'],
        'S': ['E'],
        'W': ['N'],
    },
    '|': {
        'N': ['N'],
        'E': ['N', 'S'],
        'S': ['S'],
        'W': ['N', 'S'],
    },
    '-': {
        'N': ['E', 'W'],
        'E': ['E'],
        'S': ['E', 'W'],
        'W': ['W'],
    }
}