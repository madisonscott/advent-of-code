import math
import re
from base_solver import BaseSolver

map_regex = "(?P<instructions>[LR]+)\n\n(?P<network>[\(\)\w\d=,\s\n]+)"
node_regex = "(?P<key>[\w\d]{3}) = \((?P<left>[\w\d]{3}), (?P<right>[\w\d]{3})\)"

class Solver(BaseSolver):

    def solve_part_one(self, input):
        instructions, network_map = get_instructions_and_network_map(input)
        end_condition = lambda n, _: n == 'ZZZ'
        return find_steps_for_node('AAA', instructions, network_map, end_condition)

    def test_input_one(self):
        return """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    def solve_part_two(self, input):
        instructions, network_map = get_instructions_and_network_map(input)
        nodes = filter(lambda n: n.endswith('A'), network_map.keys())

        # check that we've reached the end of the instruction set too
        end_condition = lambda n, i: n.endswith('Z') and i == 0
        step_counts = [ find_steps_for_node(n, instructions, network_map, end_condition) for n in nodes ]
        return math.lcm(*step_counts)

    def test_input_two(self):
        return """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def get_instructions_and_network_map(input):
    match = re.match(map_regex, input)
    instructions = match.group('instructions')
    network = match.group('network')
    network_map = {}

    for line in network.split('\n'):
        node_match = re.match(node_regex, line)
        node_key = node_match.group('key')
        network_map[node_key] = (node_match.group('left'), node_match.group('right'))

    return (instructions, network_map)

def find_steps_for_node(node, instructions, network_map, end_condition):
    steps = 0
    i = 0
    instructions_length = len(instructions)
    while True:
        instruction = instructions[i]
        tuple_index = 0 if instruction == 'L' else 1
        node = network_map[node][tuple_index]
        steps += 1

        i = (i + 1) % instructions_length

        if end_condition(node, i):
            return steps