import math
import os
import sys
from pathlib import Path

def get_earliest_departure_timestamp_from_input(input):
    return int(input.split('\n')[0])

def get_available_bus_ids_from_input(input):
    bus_ids = input.split('\n')[1].split(',')
    valid_bus_ids = list(filter(lambda x: x != 'x', bus_ids))
    return list(map(int, valid_bus_ids))

def find_next_arrival_of_bus_after_time(bus_id, target_time):
    return math.ceil(target_time / bus_id) * bus_id

def find_first_bus(earliest_departure, bus_ids):
    next_bus_id = -1
    next_bus_timestamp = sys.maxsize

    for bus_id in bus_ids:
        next_arrival_of_bus = find_next_arrival_of_bus_after_time(
            bus_id, earliest_departure)

        if next_arrival_of_bus < next_bus_timestamp:
            next_bus_id = bus_id
            next_bus_timestamp = next_arrival_of_bus

    return (next_bus_timestamp - earliest_departure) * next_bus_id


def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    earliest_departure = get_earliest_departure_timestamp_from_input(input)
    bus_ids = get_available_bus_ids_from_input(input)
    print(find_first_bus(earliest_departure, bus_ids))



if __name__ == '__main__':
    main()
