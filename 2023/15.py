from base_solver import BaseSolver
from collections import defaultdict
import re

step_regex="(?P<label>\w+)(?P<op>[-=]{1})(?P<focal_len>\d{0,1})"

class Solver(BaseSolver):

    def solve_part_one(self, input):
        steps = input.split(',')
        total = 0
        for step in steps:
            total += get_hash(step)
        return total

    def test_input_one(self):
        return """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

    def solve_part_two(self, input):
        steps = input.split(',')

        boxes = defaultdict(lambda: ([], {}))
        for step in steps:
            matches = re.match(step_regex, step)
            label, op = matches.group('label'), matches.group('op')
            box = get_hash(label)
            ordering, label_to_focal_len = boxes[box]

            if op == '-' and label in label_to_focal_len:
                del label_to_focal_len[label]
                ordering.remove(label)
            elif op == '=':
                focal_len = int(matches.group('focal_len'))
                if label not in label_to_focal_len:
                    ordering.append(label)
                label_to_focal_len[label] = focal_len

        total = 0
        for box_key in boxes:
            box_num = box_key + 1
            ordering, label_to_focal_len = boxes[box_key]
            for i in range(len(ordering)):
                total += box_num * (i + 1) * label_to_focal_len[ordering[i]]

        return total

def get_hash(step):
    hash = 0
    for char in step:
        hash += ord(char)
        hash *= 17
        hash %= 256
    return hash
