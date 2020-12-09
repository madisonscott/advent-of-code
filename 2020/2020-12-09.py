import os
from pathlib import Path
from utils.sums import find_n_numbers_summing_to

def get_ints_front_input(input):
    return [ int(line) for line in input.split('\n') ]

def find_first_invalid_xmas_number(numbers, preamble_len):
    for i in range(preamble_len, len(numbers)):
        current_number = numbers[i]
        previous_n_numbers = numbers[i-preamble_len:i]

        current_number_addends = find_n_numbers_summing_to(
            previous_n_numbers, 2, current_number)

        if current_number_addends == None:
            return current_number

    return None

def find_contiguous_numbers_summing_to(numbers, target):
    for segment_len in range(2, len(numbers)):
        for segment_start in range(len(numbers) - segment_len):
            segment_end = segment_start + segment_len

            segment = numbers[segment_start:segment_end]
            segment_sum = sum(segment)

            if segment_sum == target:
                return segment

    return []

def sum_min_and_max(numbers):
    return min(numbers) + max(numbers)

def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    numbers = get_ints_front_input(input)
    first_invalid_number = find_first_invalid_xmas_number(numbers, 25)
    print(first_invalid_number)

    invalid_number_addends = find_contiguous_numbers_summing_to(
        numbers, first_invalid_number)
    print(sum_min_and_max(invalid_number_addends)) 

if __name__ == '__main__':
    main()
