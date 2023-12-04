import re
from typing import Set

from base_solver import BaseSolver

cardRegex = "Card\s+(?P<cardId>[0-9]+):\s+(?P<winningNumbers>[\d\s]+)\s\|\s+(?P<myNumbers>[\d\s]+)"

class Solver(BaseSolver):

    def solve_part_one(self, input):
        total = 0

        for card in input.split('\n'):
            cardMatch = re.match(cardRegex, card)
            winners = get_winning_number_count(
                cardMatch.group('winningNumbers'), cardMatch.group('myNumbers'))
            total += 2 ** (winners - 1) if winners > 0 else 0

        return total

    def test_input_one(self):
        return """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    def solve_part_two(self, input):
        cards = input.split('\n')
        cards_won_by_card = [ 0 for _ in cards ]

        for card in reversed(cards):
            cardMatch = re.match(cardRegex, card)
            # Use 0-indexing instead of 1
            card_id = int(cardMatch.group('cardId')) - 1
            overlap_count = get_winning_number_count(
                cardMatch.group('winningNumbers'), cardMatch.group('myNumbers'))

            for i in range(1, overlap_count + 1):
                cards_won_by_card[card_id] += 1 + cards_won_by_card[card_id + i]

        return len(cards) + sum(cards_won_by_card)

def get_winning_number_count(winning_numbers_str, my_numbers_str):
    winningNumbers = get_number_set(winning_numbers_str)
    myNumbers = get_number_set(my_numbers_str)

    intersection = winningNumbers.intersection(myNumbers)
    return len(intersection)

def get_number_set(number_str: str) -> Set[str]:
    return set(filter(lambda n: len(n) > 0 , number_str.split(" ")))