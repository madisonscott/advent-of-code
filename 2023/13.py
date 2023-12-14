from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        patterns = input.strip().split('\n\n')

        total = 0
        for pattern in patterns:
            total += (
                find_mirror_location(get_cols(pattern)) or
                100 * find_mirror_location(get_rows(pattern))
            )

        return total

    def test_input_one(self):
        return """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

    def solve_part_two(self, input):
        patterns = input.strip().split('\n\n')

        total = 0
        for pattern in patterns:
            skip_col = find_mirror_location(get_cols(pattern))
            skip_row = find_mirror_location(get_rows(pattern))

            total += (
                find_mirror_location_with_smudge(get_cols(pattern), skip_col) or
                100 * find_mirror_location_with_smudge(get_rows(pattern), skip_row)
            )

        return total

def get_rows(pattern):
    return pattern.split('\n')

def get_cols(pattern):
    rows = get_rows(pattern)
    cols = []
    for i in range(len(rows[0])):
        cols.append(''.join([ row[i] for row in rows ]))
    return cols

def find_mirror_location(lines):
    for i in range(len(lines) - 1):
        # Check if right neighbor is equivalent
        if (lines[i] != lines[i + 1]):
            continue

        #If it is, confirm that the rest of the lines are equal
        before_width = i + 1
        mirrored_width = min(before_width, len(lines) - before_width)

        before_start = i - mirrored_width + 1
        after_start = before_start + mirrored_width
        before = lines[before_start:after_start]
        after = lines[after_start:after_start + mirrored_width]

        if before == after[::-1]:
            return before_width

    return None

def find_mirror_location_with_smudge(lines, skip_before_width):
    for i in range(len(lines) - 1):
        before_width = i + 1
        if before_width == skip_before_width:
            continue

        mirrored_width = min(before_width, len(lines) - before_width)
        found_smudge = False

        for j in range(mirrored_width):
            before_line = lines[i - j]
            after_line = lines[i + 1 + j]
            edit_distance = levenshteinDistance(before_line, after_line)

            if edit_distance > 1:
                # Lines are too different, this ain't it
                found_smudge = False
                break
            elif found_smudge and edit_distance != 0:
                # We already found one difference, we can't accept another
                found_smudge = False
                break
            elif not found_smudge and edit_distance == 1:
                # We found the first smudge, carry on
                found_smudge = True

        if found_smudge:
            return before_width

    return None

# Haha I stole this and then realized it was overkill oh well
# https://stackoverflow.com/questions/2460177/edit-distance-in-python
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def print_lines(lines):
    [ print(line) for line in lines ]