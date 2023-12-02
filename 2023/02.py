import functools
import operator
import re

from base_solver import BaseSolver

gameRegex = "Game (?P<gameId>[0-9]+): (?P<roundData>.*)"
roundRegex = "(?P<num>\d+) (?P<color>blue|green|red)"

class Solver(BaseSolver):

    def solve_part_one(self, input):
        total = 0;
        games = input.split('\n')

        max_colors = {
            'red': 12,
            'green': 13,
            'blue': 14
        }

        for game in games:
            gameMatch = re.match(gameRegex, game)
            rounds = gameMatch.group('roundData').split(';')

            possible = True
            for round in rounds:
                matches = re.finditer(roundRegex, round)
                for match in matches:
                    if int(match.group('num')) > max_colors[match.group('color')]:
                        possible = False
                        break

                if not possible:
                    break

            if possible:
                total += int(gameMatch.group('gameId'))

        return total

    def solve_part_two(self, input):
        total = 0;
        games = input.split('\n')

        for game in games:
            gameMatch = re.match(gameRegex, game)
            rounds = gameMatch.group('roundData').split(';')

            color_minimums = {
                'red': 0,
                'green': 0,
                'blue': 0
            }

            for round in rounds:
                matches = re.finditer(roundRegex, round)
                for match in matches:
                    num = int(match.group('num'))
                    color = match.group('color')
                    if num > color_minimums[color]:
                        color_minimums[color] = num

            game_power = functools.reduce(operator.mul, list(color_minimums.values()))
            total += game_power

        return total

    def test_input_one(self):
        return """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""