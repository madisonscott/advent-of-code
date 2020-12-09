import os
from pathlib import Path
from utils.sums import find_n_numbers_summing_to

def split_input_to_nums_list(input):
    return [ int(num) for num in input.split('\n') ]

def solve_puzzle(input, target, n):
    numbers = split_input_to_nums_list(input)
    chosen_numbers = find_n_numbers_summing_to(numbers, target, n)

    result = 1
    for number in chosen_numbers:
        result *= number

    return result

def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    print(solve_puzzle(input, 2, 2020))
    print(solve_puzzle(input, 3, 2020))

if __name__ == '__main__':
    main()
