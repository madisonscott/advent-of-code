import os
from pathlib import Path

def get_forest_from_input(input):
    lines = input.split('\n')
    return [ [ char for char in line ] for line in lines ]

def is_tree(forest, x, y):
    return forest[y][x] == '#'

def find_trees_in_path(input, slope_x, slope_y):
    forest = get_forest_from_input(input)
    height = len(forest)
    width = len(forest[0])

    trees_encountered = 0
    x_position = 0

    for y_position in range(0, height, slope_y):
        trees_encountered += 1 if is_tree(forest, x_position, y_position) else 0
        x_position = (x_position + slope_x) % width

    return trees_encountered

def solve_puzzle(input, slopes):
    result = 1
    
    for (x, y) in slopes:
        trees = find_trees_in_path(input, x, y)
        result *= trees

    return result

def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    print(solve_puzzle(input, [(3, 1)])) 

    slopes_2 = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]

    print(solve_puzzle(input, slopes_2))

if __name__ == '__main__':
    main()
