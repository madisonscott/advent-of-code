import os
from pathlib import Path

def get_directions_from_input(input):
    return [ (line[0], int(line[1:])) for line in input.split('\n') ]

def get_multipliers_for_direction(direction):
    if direction == 'N':
        return (0, 1)
    elif direction == 'E':
        return (1, 0)
    elif direction == 'S':
        return (0, -1)
    elif direction == 'W':
        return (-1, 0)

def move_units_in_direction(units, direction, current_position):
    current_x, current_y = current_position
    x_multiplier, y_multiplier = get_multipliers_for_direction(direction)
    return (current_x + units * x_multiplier, current_y + units * y_multiplier)

def turn_degrees_in_direction(degrees, direction, current_direction):
    cardinal_directions = ['N', 'E', 'S', 'W']
    current_direction_idx = cardinal_directions.index(current_direction)

    steps = int(degrees / 90)
    direction_multiplier = 1 if direction == 'R' else -1
    next_direction_index = (current_direction_idx + steps * direction_multiplier) % 4

    return cardinal_directions[next_direction_index]


def execute_directions(directions):

    currently_facing = 'E'
    current_position = (0, 0)

    for (direction, units) in directions:
        if direction in ['L', 'R']:
            currently_facing = turn_degrees_in_direction(
                units, direction, currently_facing)
            print(f'turning {currently_facing}')

        elif direction == 'F':
            current_position = move_units_in_direction(
                units, currently_facing, current_position)
            print(f'moving {currently_facing} {units} to {current_position}')

        else:
            current_position = move_units_in_direction(
                units, direction, current_position)
            print(f'moving {direction} {units} to {current_position}')

    return current_position

def rotate_waypoint_in_direction(degrees, direction, current_waypoint):
    if direction == 'L':
        degrees = (degrees * -1 + 4 * 90)

    waypoint_x, waypoint_y = current_waypoint

    if degrees == 0:                     # (10, 4)
        return (waypoint_x, waypoint_y)
    elif degrees == 90:                 # (4, -10)
        return (waypoint_y, -1 * waypoint_x)
    elif degrees == 180:                # (-10, -4)
        return (-1 * waypoint_x, -1 * waypoint_y)
    elif degrees == 270:
        return (-1 * waypoint_y, waypoint_x)

def move_units_to_waypoint(units, current_waypoint, current_position):
    current_x, current_y = current_position
    waypoint_x, waypoint_y = current_waypoint

    return (current_x + units * waypoint_x, current_y + units * waypoint_y)

def execute_directions_with_waypoint(directions):

    current_waypoint = (10, 1)
    current_position = (0, 0)

    for (direction, units) in directions:
        if direction in ['L', 'R']:
            current_waypoint = rotate_waypoint_in_direction(
                units, direction, current_waypoint)
            print(f'rotating wp {direction} {units} to {current_waypoint}')

        elif direction == 'F':
            current_position = move_units_to_waypoint(
                units, current_waypoint, current_position)
            print(f'moving toward waypoint {units} to {current_position}')

        else:
            current_waypoint = move_units_in_direction(
                units, direction, current_waypoint)
            print(f'moving wp {direction} {units} to {current_waypoint}')

    return current_position



def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    directions = get_directions_from_input(input)
    x, y = execute_directions(directions)
    print(abs(x) + abs(y))

    wp_x, wp_y = execute_directions_with_waypoint(directions)
    print(abs(wp_x) + abs(wp_y))


if __name__ == '__main__':
    main()
