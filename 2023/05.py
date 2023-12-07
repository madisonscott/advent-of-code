import re
import sys
from base_solver import BaseSolver

mapRegex = "seeds: (?P<seeds>[0-9\s]+)\n\nseed-to-soil map:\n(?P<seedToSoil>[0-9\s]+)\n\nsoil-to-fertilizer map:\n(?P<soilToFert>[0-9\s]+)\n\nfertilizer-to-water map:\n(?P<fertToWater>[0-9\s]+)\n\nwater-to-light map:\n(?P<waterToLight>[0-9\s]+)\n\nlight-to-temperature map:\n(?P<lightToTemp>[0-9\s]+)\n\ntemperature-to-humidity map:\n(?P<tempToHum>[0-9\s]+)\n\nhumidity-to-location map:\n(?P<humToLoc>[0-9\s]+)"

mapping_order = [
    'seedToSoil',
    'soilToFert',
    'fertToWater',
    'waterToLight',
    'lightToTemp',
    'tempToHum',
    'humToLoc',
]

class Solver(BaseSolver):

    def solve_part_one(self, input):
        match = re.match(mapRegex, input)
        map_of_mappings = get_all_mappings(match)

        seeds = [ int(s) for s in match.group('seeds').split(' ') ]
        return get_min_location_from_seeds(map_of_mappings, seeds)

    def solve_part_two(self, input):
        match = re.match(mapRegex, input)
        map_of_mappings = get_all_mappings(match)

        seed_ranges = [ int(s) for s in match.group('seeds').split(' ') ]

        current_min = sys.maxsize
        for i in range(0, len(seed_ranges), 2):
            start_seed = seed_ranges[i]
            range_len = seed_ranges[i + 1]
            print(start_seed, range_len)

            min_in_batch = get_min_location_from_seeds(map_of_mappings, range(start_seed, start_seed + range_len))
            current_min = min(current_min, min_in_batch)

            # This solution takes an actual eternity, but we can watch it as it works and
            # keep submitting guesses lol?
            print('current min', current_min)

        return current_min

    def test_input_one(self):
        return """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

def get_all_mappings(match):
    map_of_mappings = {}
    for mapping_name in mapping_order:
        map_of_mappings[mapping_name] = get_mapping_from_match(match, mapping_name)
    return map_of_mappings


def get_min_location_from_seeds(map_of_mappings, seeds):
    min_location = sys.maxsize
    for seed in seeds:
        val = seed
        for mapping_name in mapping_order:
            mapping = map_of_mappings[mapping_name]
            val = get_value_from_map(mapping, val)

        if val < min_location:
            min_location = val

    return min_location

def get_mapping_from_match(match, mapping_name):
    descriptors = match.group(mapping_name).split('\n')
    return get_mapping_from_mapping_descriptors(descriptors)

def get_mapping_from_mapping_descriptors(descriptors):
    mapping = []
    for descriptor in descriptors:
        dest, start, range_len = descriptor.split(" ")
        mapping.append((int(start), int(start) + int(range_len), int(dest)))

    return sorted(mapping, key = lambda x: x[0])

def get_value_from_map(mapping, input):
    for start, end_exc, dest in mapping:
        if input < start:
            break
        elif input < end_exc:
            diff = input - start
            return dest + diff

    return input

