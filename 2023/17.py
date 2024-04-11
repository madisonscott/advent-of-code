from base_solver import BaseSolver
import sys

class Solver(BaseSolver):

    def solve_part_one(self, input):
        map = [ [ col for col in row ] for row in input.strip().split('\n') ]
        total = 0
        return total

    def test_input_one(self):
        return """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

    def solve_part_two(self, input):
      total = 0
      return total

    def test_input_two(self):
        return """TEST_INPUT"""

def find_lowest_heat_loss(map, y, x, current_dir_coords):
    if not (0 <= y < len(map) or 0 <= x < len(map[y])):
        return sys.maxsize

    if y == len(map) - 1 and x == len(map[0]) - 1:
        return map[y][x]

    # next_

    return min([

    ])

dir_coords = {
    (-1, 0): [(0, -1), (-1, 0), (0, 1)],
    (0, 1): [(-1, 0), (0, 1), (1, 0)],
    (1, 0): [(0, 1), (1, 0), (0, -1)],
    (0, -1): [(1, 0), (0, -1), (-1, 0)],
}