import re
from base_solver import BaseSolver

class Solver(BaseSolver):

    def solve_part_one(self, input):
        total = 0;
        lines = input.split('\n')
        regex = "[0-9]{1}"

        for line in lines:
            numbers = re.findall(regex, line)
            total += int(numbers[0] + numbers[-1])

        return total

    def test_input_one(self):
        return """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    def solve_part_two(self, input):
      total = 0;
      lines = input.split('\n')
      regex = "(?=([0-9]{1}|one|two|three|four|five|six|seven|eight|nine))"

      numbers_to_numbers = {
          'one': '1',
          'two': '2',
          'three': '3',
          'four': '4',
          'five': '5',
          'six': '6',
          'seven': '7',
          'eight': '8',
          'nine': '9',
      }

      for line in lines:
          numbers = re.findall(regex, line)
          total += int(
              (numbers_to_numbers[numbers[0]] if numbers[0] in numbers_to_numbers else numbers[0]) +
              (numbers_to_numbers[numbers[-1]] if numbers[-1] in numbers_to_numbers else numbers[-1])
          )

      return total

    def test_input_two(self):
        return """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
