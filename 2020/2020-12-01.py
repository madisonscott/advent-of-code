import os
from pathlib import Path
    
def split_input_to_nums_list(input):
    return [ int(num) for num in input.split('\n') ]

def find_n_numbers_summing_to(numbers, n, target):
    return _find_n_numbers_summing_to_helper(numbers, n, target, -1, [])

def _find_n_numbers_summing_to_helper(numbers, n, target, current_index, numbers_to_examine):
    if n == 0 or current_index == len(numbers):
        result = sum(numbers_to_examine)

        if result == target:
            return numbers_to_examine
        else:
            return None

    for i in range(current_index + 1, len(numbers)):
        new_numbers_to_examine = [ num for num in numbers_to_examine ]
        new_numbers_to_examine.append(numbers[i])

        result = _find_n_numbers_summing_to_helper(numbers, n - 1, target, i, new_numbers_to_examine)

        if result != None:
            return result

    return None

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
