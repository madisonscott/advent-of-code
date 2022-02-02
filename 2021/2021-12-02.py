import os
from pathlib import Path

def split_input_to_directions_list(input):
    return [ line.split(' ') for line in input.split('\n') ]

def solve_puzzle(input):
    directions = split_input_to_directions_list(input)

    horizontal_position = 0
    depth = 0

    for [direction, val] in directions:
        if direction == 'forward':
            horizontal_position += int(val)
        elif direction == 'up':
            depth -= int(val)
        elif direction == 'down':
            depth += int(val)

    return horizontal_position * depth

def solve_second_puzzle(input):
    directions = split_input_to_directions_list(input)

    horizontal_position = 0
    depth = 0
    aim = 0

    for [direction, val] in directions:
        if direction == 'forward':
            horizontal_position += int(val)
            depth += aim * int(val)
        elif direction == 'up':
            aim -= int(val)
        elif direction == 'down':
            aim += int(val)

    return horizontal_position * depth


def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    print(solve_puzzle(input))
    print(solve_second_puzzle(input))

if __name__ == '__main__':
    main()
