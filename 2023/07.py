from collections import defaultdict
import operator
from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        total = 0

        hands = [ line.split(" ") for line in input.split('\n') ]

        hand_data = []
        for hand, bid in hands:
            hand_value = hand_type_value[get_hand_type(hand)]
            hand_signature = get_hand_signature(hand, card_value_jacks)
            hand_data.append((hand_value, hand_signature, int(bid)))

        sorted_hand_data = sorted(hand_data, key = operator.itemgetter(0, 1))

        hand_count = len(sorted_hand_data)
        for i in range(hand_count):
            total += (hand_count - i) * sorted_hand_data[i][2]

        return total

    def test_input_one(self):
        return """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    def solve_part_two(self, input):
        total = 0

        hands = [ line.split(" ") for line in input.split('\n') ]

        hand_data = []
        for hand, bid in hands:
            hand_value = hand_type_value[get_best_hand_type_with_joker(hand)]
            hand_signature = get_hand_signature(hand, card_value_jokers)
            hand_data.append((hand_value, hand_signature, int(bid)))

        sorted_hand_data = sorted(hand_data, key = operator.itemgetter(0, 1))

        hand_count = len(sorted_hand_data)
        for i in range(hand_count):
            total += (hand_count - i) * sorted_hand_data[i][2]

        return total

hand_type_value = {
    '5': 0,
    '41': 1,
    '32': 2,
    '311': 3,
    '221': 4,
    '2111': 5,
    '11111': 6
}

card_value_jacks = {
    'A': 'a',
    'K': 'b',
    'Q': 'c',
    'J': 'd',
    'T': 'e',
    '9': 'f',
    '8': 'g',
    '7': 'h',
    '6': 'i',
    '5': 'j',
    '4': 'k',
    '3': 'l',
    '2': 'm',
}

card_value_jokers = {
    'A': 'a',
    'K': 'b',
    'Q': 'c',
    'T': 'e',
    '9': 'f',
    '8': 'g',
    '7': 'h',
    '6': 'i',
    '5': 'j',
    '4': 'k',
    '3': 'l',
    '2': 'm',
    'J': 'n',
}

def get_hand_type(hand):
    card_count = defaultdict(int)
    for card in hand:
        card_count[card] += 1

    return ''.join([ str(n) for n in sorted(card_count.values(), reverse = True) ])

def get_best_hand_type_with_joker(hand):
    card_count = defaultdict(int)
    for card in hand:
        card_count[card] += 1

    num_jokers = card_count['J']
    del card_count['J']

    current_hand_sorted = sorted(card_count.values(), reverse = True)
    current_hand_type = ''.join([ str(n) for n in current_hand_sorted ])

    if num_jokers == 0:
        return current_hand_type
    elif num_jokers == 5:
        return '5'
    else:
        current_hand_sorted[0] += num_jokers
        return ''.join([ str(n) for n in current_hand_sorted ])

def get_hand_signature(hand, card_value_mapping):
    return ''.join([ card_value_mapping[c] for c in hand ])