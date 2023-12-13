from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        spring_rows = parse_input(input)

        total = 0
        for row, broken_recs in spring_rows:
            total += count_possible_rows(row, broken_recs)

        return total

    def test_input_one(self):
        return """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    def solve_part_two(self, input):
        spring_rows = parse_input(input, expanded = True)

        total = 0
        for row, broken_recs in spring_rows:
            print(row)
            print(broken_recs)
            possible = count_possible_rows(row, broken_recs)
            print(possible)
            total += possible

        return total


def parse_input(input, expanded = False):
    spring_rows = []
    for row in input.split('\n'):
        spring_conditions, broken_recs = row.split(' ')
        if expanded:
            spring_rows.append((
                list('?'.join([ spring_conditions ] * 5)),
                [ int(n) for n in broken_recs.split(',') * 5 ])
            )
        else:
            spring_rows.append((
                list(spring_conditions),
                [ int(n) for n in broken_recs.split(',') ])
            )
    return spring_rows


def count_possible_rows(row, actual_broken_recs, possible_row = ''):
    if len(row) == len(possible_row):
        if is_matching_arrangement(possible_row, actual_broken_recs):
            return 1
        return 0
    elif not is_possible_arrangement(possible_row, actual_broken_recs):
        return 0

    i = len(possible_row)
    if row[i] == '?':
        return (
            count_possible_rows(row, actual_broken_recs, possible_row + '.') +
            count_possible_rows(row, actual_broken_recs, possible_row + '#')
        )
    else:
        return count_possible_rows(row, actual_broken_recs, possible_row + row[i])

def is_possible_arrangement(possible_row, actual_broken_recs):
    possible_groups = possible_row.split('.')
    possible_incomplete_end = possible_row.endswith('#')
    possible_broken_recs = [ len(g) for g in possible_groups if g ]

    num_possible = len(possible_broken_recs)
    if num_possible > len(actual_broken_recs):
        return False

    for i in range(num_possible):
        possible = possible_broken_recs[i]
        actual = actual_broken_recs[i]

        if possible_incomplete_end and i == num_possible - 1 and possible < actual:
            return True
        elif possible != actual:
            return False

    return True

def is_matching_arrangement(possible_row, actual_broken_recs):
    possible_groups = possible_row.split('.')
    possible_broken_recs = [ len(g) for g in possible_groups if g ]
    return possible_broken_recs == actual_broken_recs
