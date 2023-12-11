from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        sequences = [ [ int(n) for n in line.split(' ') ] for line in input.split('\n') ]

        total = 0
        for sequence in sequences:
            total += extrapolate_next_value(sequence)
        return total

    def test_input_one(self):
        return """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    def solve_part_two(self, input):
        sequences = [ [ int(n) for n in line.split(' ') ] for line in input.split('\n') ]

        total = 0
        for sequence in sequences:
            total += extrapolate_previous_value(sequence)
        return total

def extrapolate_next_value(sequence):
    last_values = [sequence[-1]]

    while not are_all_zero(sequence):
        sequence = get_sequence_differences(sequence)
        last_values.append(sequence[-1])

    return sum(last_values)

def extrapolate_previous_value(sequence):
    first_values = [sequence[0]]

    while not are_all_zero(sequence):
        sequence = get_sequence_differences(sequence)
        first_values.append(sequence[0])

    extrapolated_value = 0
    while len(first_values) > 0:
        extrapolated_value = first_values.pop() - extrapolated_value

    return extrapolated_value

def get_sequence_differences(sequence):
    return [ sequence[i] - sequence[i - 1] for i in range(1, len(sequence)) ]

def are_all_zero(sequence):
    for n in sequence:
        if n != 0:
            return False
    return True