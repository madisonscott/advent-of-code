from base_solver import BaseSolver
from typing import List, Tuple

class Solver(BaseSolver):

    def solve_part_one(self, input):
        total = 0

        board = get_board_from_input(input)

        for y in range(len(board)):
            part_numbers = find_part_numbers_in_row(board, y)
            total += sum(part_numbers)

        return total

    def test_input_one(self):
        return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    def solve_part_two(self, input):
        board = get_board_from_input(input)
        potential_gear_numbers = []

        for y in range(len(board)):
            potential_gear_numbers.extend(find_potential_gear_parts_in_row(board, y))

        gear_ratios = get_gear_ratios(potential_gear_numbers)

        return sum(gear_ratios)

def find_part_numbers_in_row(board: List[List[str]], y: int) -> List[int]:
    x = 0
    row = board[y]
    part_numbers: List[int] = []

    current_number_string = ''
    is_part_number = False

    while x <= len(row):
        if x < len(row) and row[x].isnumeric():
            current_number_string += row[x]
            is_part_number = is_part_number or has_adjacent_symbol(board, y, x)

        elif len(current_number_string) > 0:
            # we just finished a number, check the endcaps for symbols if needed
            left_end = x - len(current_number_string) - 1
            if (is_part_number or
                has_adjacent_symbol(board, y, left_end, True) or
                has_adjacent_symbol(board, y, x, True)):
                part_numbers.append(int(current_number_string))

            # reset
            current_number_string = ''
            is_part_number = False

        x += 1

    return part_numbers

def has_adjacent_symbol(board: List[List[str]], y: int, x: int, is_endcap: bool = False) -> bool:
    if is_endcap:
        if not (x >= 0 and x < len(board[y])):
            # x is out of bounds and we should stop looking
            return False

        if is_symbol(board[y][x]):
            return True

    y_above = y - 1
    if y_above >= 0 and is_symbol(board[y_above][x]):
        return True

    y_below = y + 1
    if y_below < len(board) and is_symbol(board[y_below][x]):
        return True

    return False

# Returns list of tuple of (number, list of asterisks)
def find_potential_gear_parts_in_row(board: List[List[str]], y: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    x = 0
    row = board[y]
    part_numbers: List[int] = []

    current_number_string = ''
    adjacent_asterisks = []

    while x <= len(row):
        if x < len(row) and row[x].isnumeric():
            current_number_string += row[x]
            adjacent_asterisks.extend(get_adjacent_asterisks(board, y, x))

        elif len(current_number_string) > 0:
            # we just finished a number, check the endcaps for symbols if needed
            left_end = x - len(current_number_string) - 1
            adjacent_asterisks.extend(get_adjacent_asterisks(board, y, left_end, True))
            adjacent_asterisks.extend(get_adjacent_asterisks(board, y, x, True))
            if len(adjacent_asterisks) > 0:
                part_numbers.append((int(current_number_string), adjacent_asterisks))

            # reset
            current_number_string = ''
            adjacent_asterisks = []

        x += 1

    return part_numbers

def get_gear_ratios(potential_gear_parts: List[Tuple[int, List[Tuple[int, int]]]]) -> List[int]:
    gear_ratios = []
    parts_by_gear_coords: dict[Tuple[int, int], List[int]] = dict()

    for part_number, potential_gear_coords in potential_gear_parts:
        for gear_coords in potential_gear_coords:
            if not gear_coords in parts_by_gear_coords:
                parts_by_gear_coords[gear_coords] = []
            parts_by_gear_coords[gear_coords].append(part_number)

    for part_numbers in parts_by_gear_coords.values():
        if len(part_numbers) == 2:
            gear_ratios.append(part_numbers[0] * part_numbers[1])

    return gear_ratios


def get_adjacent_asterisks(board: List[List[str]], y: int, x: int, is_endcap: bool = False) -> List[Tuple[int, int]]:
    asterisks: List[Tuple[int, int]] = []

    if is_endcap:
        if not (x >= 0 and x < len(board[y])):
            # x is out of bounds and we should stop looking
            return []

        if board[y][x] == '*':
            asterisks.append((y, x))

    y_above = y - 1
    if y_above >= 0 and board[y_above][x] == '*':
        asterisks.append((y_above, x))

    y_below = y + 1
    if y_below < len(board) and board[y_below][x] == '*':
        asterisks.append((y_below, x))

    return asterisks

def is_symbol(char: str) -> bool:
    return not char.isalnum() and char != '.'

def get_board_from_input(input):
    return [ [ space for space in row ] for row in input.split('\n') ]