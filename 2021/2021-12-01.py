import os
from pathlib import Path

def split_input_to_nums_list(input):
    return [ int(num) for num in input.split('\n') ]

def solve_puzzle(input, window_size):
    numbers = split_input_to_nums_list(input)
    times_increased = 0

    for i in range(1, len(numbers) - window_size + 1):
        current_window = sum(numbers[i:i+window_size])
        prev_window = sum(numbers[i-1:i-1+window_size])

        if current_window > prev_window:
            times_increased += 1

    return times_increased

def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    print(solve_puzzle(input, 1))
    print(solve_puzzle(input, 3))

if __name__ == '__main__':
    main()
