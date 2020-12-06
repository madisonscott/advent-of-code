import os
from pathlib import Path

def get_int_from_binary_like_notation(notation, _0_replacement, _1_replacement):
    binary_string = '0b'

    for char in notation:
        if char == _0_replacement:
            binary_string += '0'
        elif char == _1_replacement:
            binary_string += '1'
        else:
            raise Exception('Invalid seat specification')

    return int(binary_string, 2)

def get_row_num(front_back_notation):
    return get_int_from_binary_like_notation(front_back_notation, 'F', 'B')

def get_seat_num(left_right_notation):
    return get_int_from_binary_like_notation(left_right_notation, 'L', 'R')

def get_seat_id(seat_specifier):
    row_num = get_row_num(seat_specifier[:7])
    seat_num = get_seat_num(seat_specifier[7:])
    return row_num * 8 + seat_num

def solve_puzzle(input):
    seat_specifiers = input.split('\n')

    seat_ids = [ get_seat_id(specifier) for specifier in seat_specifiers ]
    seat_ids_set = set(seat_ids)

    min_seat_id = min(seat_ids)
    max_seat_id = max(seat_ids)
    print(max_seat_id)

    # Skip the missing seats at the front of the plane a la puzzle constraints.
    # Wouldn't fly in real world but oh well :-)
    # Pun intended.
    for seat_id in range(min_seat_id, max_seat_id):
        if seat_id not in seat_ids_set:
            return seat_id

    return -1

def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    print(solve_puzzle(input)) 

if __name__ == '__main__':
    main()
