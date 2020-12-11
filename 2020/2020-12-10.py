import os
from collections import defaultdict
from pathlib import Path


def get_adapters_front_input(input):
    return [ int(line) for line in input.split('\n') ]


def find_distribution_of_differences(adapters):
    wall_joltage = 0
    device_joltage = max(adapters) + 3

    adapters.append(wall_joltage)
    adapters.append(device_joltage)
    sorted_adapters = sorted(adapters)

    differences = defaultdict(lambda: 0)
    last_joltage = wall_joltage

    for joltage in sorted_adapters:
        diff = joltage - last_joltage
        differences[diff] += 1

        last_joltage = joltage

    return differences


# Like, really slow.
def find_all_adapter_arrangements_the_slow_way(adapters):
    sorted_adapters = sorted(adapters)
    device_joltage = max(sorted_adapters) + 3

    return _find_all_adapter_arrangements_the_slow_way_helper(
        0, sorted_adapters, device_joltage)


def _find_all_adapter_arrangements_the_slow_way_helper(
    last_joltage, adapters_remaining, target):

    allowed_difference = 3

    if last_joltage + allowed_difference >= target:
        return 1

    arrangements = 0
    for i in range(min(allowed_difference, len(adapters_remaining))):
        adapter = adapters_remaining[i]

        if adapter - last_joltage > allowed_difference:
            break

        arrangements += _find_all_adapter_arrangements_the_slow_way_helper(
            adapter, adapters_remaining[i+1:], target)

    return arrangements


def find_all_adapter_arrangements(adapters):
    wall_joltage = 0
    device_joltage = max(adapters) + 3

    # Start with zero results for all joltages from zero to the device joltage
    dp = [ 0 for i in range(device_joltage+1) ]
    dp[device_joltage] = 1

    # Sort adapters in descending order to start at the end
    adapters.append(wall_joltage)
    sorted_adapters = sorted(adapters)
    sorted_adapters.reverse()

    _find_all_adapter_arrangements_helper(device_joltage, sorted_adapters, dp)

    return dp[0]


def _find_all_adapter_arrangements_helper(target, adapters_desc, dp):
    # If no more adapters, we're done!
    if len(adapters_desc) == 0:
        return

    # Adapters can accept an input joltage no less than three below their
    # own joltage output
    allowed_difference = 3

    # We can examine at most the next three adapters (due to the allowed
    # difference between adapter input and output) or the remaining adapters
    # if fewer than three
    for i in range(min(allowed_difference, len(adapters_desc))):
        adapter = adapters_desc[i]

        # We can only use an adapter if its output is within the allowed
        # difference of the target output
        if target - adapter > allowed_difference:
            break

        # For this adapter, we can use any of the routes through adapters with
        # outputs within the allowed difference of this adapter's output
        dp[adapter] = sum(dp[adapter+1:adapter+allowed_difference+1])

    # Determine the routes possible through the next adapter
    next_target = adapters_desc[0]
    adapters_under_next = adapters_desc[1:]
    _find_all_adapter_arrangements_helper(next_target, adapters_under_next, dp)


def main():
    input_file_name = f'{Path(__file__).stem}.txt'
    input_file_path = os.path.join('input', input_file_name)

    input = ''
    with open(input_file_path) as f:
        input = f.read()

    adapters = get_adapters_front_input(input)
    difference_dist = find_distribution_of_differences(adapters)
    print(difference_dist[1] * difference_dist[3])

    print(find_all_adapter_arrangements(adapters))

if __name__ == '__main__':
    main()
