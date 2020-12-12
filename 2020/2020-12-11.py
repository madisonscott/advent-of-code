import os
from copy import deepcopy
from pathlib import Path

FLOOR = '.'
EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"

def get_layout_from_input(input):
    return [ [ space for space in row ] for row in input.split('\n') ]

def pretty_print_layout(layout):
    for row in layout:
        print(''.join(row))

def is_within_layout(layout, row, col):
    height = len(layout)
    width = len(layout[0])

    return 0 <= row and row < height and 0 <= col and col < width

def is_seat(layout, row, col):
    return layout[row][col] != FLOOR

def is_occupied_seat(layout, row, col):
    return layout[row][col] == OCCUPIED_SEAT

def get_num_occupied_neighbors(layout, row, col):
    directions = [-1, 0, 1]
    occupied_neighbors = 0

    for row_diff in directions:
        for col_diff in directions:
            neighbor_row = row + row_diff
            neighbor_col = col + col_diff

            if (not (row_diff == 0 and col_diff == 0)
                and is_within_layout(layout, neighbor_row, neighbor_col)
                and is_occupied_seat(layout, neighbor_row, neighbor_col)
            ):
                occupied_neighbors += 1

    return occupied_neighbors

def is_first_space_in_sight_occupied(
    layout, row, row_direction, col, col_direction):

    spaces_away = 1

    while True:
        next_row = row + row_direction * spaces_away
        next_col = col + col_direction * spaces_away

        # We've reached the edge of the board
        if not is_within_layout(layout, next_row, next_col):
            break

        if is_seat(layout, next_row, next_col):
            return is_occupied_seat(layout, next_row, next_col)

        spaces_away += 1

    return False

def get_num_occupied_seats_in_sight(layout, row, col):
    directions = [-1, 0, 1]
    occupied_neighbors = 0

    for row_direction in directions:
        for col_direction in directions:
            if (not (row_direction == 0 and col_direction == 0)
                and is_first_space_in_sight_occupied(
                    layout, row, row_direction, col, col_direction
                )
            ):
                occupied_neighbors += 1

    return occupied_neighbors

def should_be_occupied_next(layout, row, col, is_strict):
    is_occupied_now = is_occupied_seat(layout, row, col)
    num_occupied_neighbors = (
        get_num_occupied_neighbors(layout, row, col)
        if is_strict
        else get_num_occupied_seats_in_sight(layout, row, col)
    )

    neighbor_limit = 4 if is_strict else 5

    if not is_occupied_now and num_occupied_neighbors == 0:
        return True
    elif is_occupied_now and num_occupied_neighbors >= neighbor_limit:
        return False
    else:
        return is_occupied_now

def get_next_layout(layout, is_strict):
    height = len(layout)
    width = len(layout[0])
    next_layout = deepcopy(layout)

    for row in range(height):
        for col in range(width):
            if not is_seat(layout, row, col):
                continue

            next_layout[row][col] = (
                OCCUPIED_SEAT
                if should_be_occupied_next(layout, row, col, is_strict)
                else EMPTY_SEAT
            )

    return next_layout

def get_stable_layout(layout, is_strict):
    i = 0

    while True:
        # Because watching a lobby simulator is p fun
        print(f'{i}:')
        pretty_print_layout(layout)
        print()

        next_layout = get_next_layout(layout, is_strict)

        if layout == next_layout:
            break

        layout = next_layout
        i += 1

    return layout

def get_num_occupied_seats(layout):
    return sum([ sum(
        [ 1 if space == OCCUPIED_SEAT else 0 for space in row ]
    ) for row in layout ])

def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    layout = get_layout_from_input(input)

    stable_strict = get_stable_layout(layout, is_strict = True)
    num_occupied_seats_strict = get_num_occupied_seats(stable_strict)

    stable_loose = get_stable_layout(layout, is_strict = False)
    num_occupied_seats_loose = get_num_occupied_seats(stable_loose)

    print(num_occupied_seats_strict)
    print(num_occupied_seats_loose)

if __name__ == '__main__':
    main()
