from base_solver import BaseSolver
import re

step_regex = "(?P<dir>[URDL]) (?P<num>\d+) \(#(?P<hex_code>[0-9a-f]{6})\)"

class Solver(BaseSolver):

    def solve_part_one(self, input):
        plan = input.strip().split('\n')
        map = [['#']]

        total = follow_steps(plan, map, True, False)
        [ print(''.join(row)) for row in map ]

        return total

    def test_input_one(self):
        return """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    def solve_part_two(self, input):
      total = 0
      return total

    def test_input_two(self):
        return """TEST_INPUT"""

def follow_steps(plan, map, should_dig, should_fill):
    y, x = (0, 0)
    start_y, start_x = y, x

    for step in plan:
        match = re.match(step_regex, step)
        dir, num = match.group('dir'), int(match.group('num'))
        d_y, d_x = dir_coords[dir]

        dug_num = 0
        dig_num = max(abs(d_y * num), abs(d_x * num))

        while dug_num < dig_num:
            y += d_y
            x += d_x

            if dir == 'L' and x < 0:
                start_x += 1
            elif dir == 'U' and y < 0:
                start_y += 1

            if should_dig:
                y, x = dig(map, y, x)
            # if fill:

            dug_num += 1

    print(start_y, start_x)
    y, x = start_y, start_x

    for step in plan:
        match = re.match(step_regex, step)
        dir, num = match.group('dir'), int(match.group('num'))
        d_y, d_x = dir_coords[dir]

        dug_num = 0
        dig_num = max(abs(d_y * num), abs(d_x * num))

        while dug_num < dig_num:
            y += d_y
            x += d_x

            dig_in_direction(map, y, x, right_coords[dir], 'R')
            dig_in_direction(map, y, x, left_coords[dir], 'L')

            dug_num += 1

        cubic_meters = 0
        for row in map:
            for col in row:
                if col == 'R' or col == '#':
                    cubic_meters += 1

        return cubic_meters

def dig(map, y, x):
    y, x = extend(map, y, x)
    map[y][x] = '#'
    # [ print(''.join(row)) for row in map ]
    # print()
    return y, x

# From 10.py
def dig_in_direction(map, y, x, dir_coords, replacement):
    rows = len(map)
    cols = len(map[0])

    queue = []
    y_d, x_d = dir_coords
    queue.append((y + y_d, x + x_d))

    while len(queue):
        y, x = queue.pop(0)
        if 0 <= y < rows and 0 <= x < cols and map[y][x] == '.':
            map[y][x] = replacement
            for y_d, x_d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                queue.append((y + y_d, x + x_d))

def extend(map, y, x):
    # print('extending to', y, x)
    if y > 0:
        for _ in range(len(map), y + 1):
            map.append([ '.' for _ in map[0] ])
    elif y < 0:
        for _ in range(y, 0):
            map.insert(0, [ '.' for _ in map[0] ])
        y = 0

    reset_x = False
    extend_x = (x + 1) - len(map[0])
    for i in range(len(map)):
        if x > 0:
            if extend_x > 0:
                map[i].extend([ '.' ] * extend_x)
        elif x < 0:
            map[i] = ([ '.' ] * abs(x)) + map[i]
            reset_x = True

    x = 0 if reset_x else x

    # print('coords now', y, x)
    return y, x

dir_coords = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1)
}

right_coords = {
    'L': (-1, 0),
    'U': (0, 1),
    'R': (1, 0),
    'D': (0, -1)
}

left_coords = {
    'R': (-1, 0),
    'D': (0, 1),
    'L': (1, 0),
    'U': (0, -1)
}
