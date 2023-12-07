import math
from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        time_line, distance_line = input.split('\n')
        times = list(filter(lambda n: len(n) > 0 , time_line.replace('Time:', '').split(' ')))
        distances = list(filter(lambda n: len(n) > 0 , distance_line.replace('Distance:', '').split(' ')))

        total = 1
        for i in range(len(times)):
            race_time = int(times[i])
            record_distance = int(distances[i])

            total *= find_ways_to_win(race_time, record_distance)

        return total

    def test_input_one(self):
        return """Time:      7  15   30
Distance:  9  40  200"""

    def solve_part_two(self, input):
        time_line, distance_line = input.split('\n')

        race_time = int(time_line.replace('Time:', '').replace(' ', ''))
        record_distance = int(distance_line.replace('Distance:', '').replace(' ', ''))

        return find_ways_to_win(race_time, record_distance)

def find_race_distance(race_time, hold_time):
    movement_time = race_time - hold_time
    return movement_time * hold_time

def find_ways_to_win(race_time, record_distance):
    ways_to_win = 0

    # start in middle and work our way outward
    halfway = math.floor(race_time / 2)
    for hold_time in range(halfway, race_time):
        if find_race_distance(race_time, hold_time) > record_distance:
            ways_to_win += 1
        else:
            break

    for hold_time in range(halfway - 1, 0, -1):
        if find_race_distance(race_time, hold_time) > record_distance:
            ways_to_win += 1
        else:
            break

    return ways_to_win
