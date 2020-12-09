def find_n_numbers_summing_to(numbers, n, target):
    return _find_n_numbers_summing_to_helper(numbers, n, target, -1, [])

def _find_n_numbers_summing_to_helper(numbers, n, target, current_index, numbers_to_examine):
    if n == 0 or current_index == len(numbers):
        result = sum(numbers_to_examine)

        if result == target:
            return numbers_to_examine
        else:
            return None

    for i in range(current_index + 1, len(numbers)):
        new_numbers_to_examine = [ num for num in numbers_to_examine ]
        new_numbers_to_examine.append(numbers[i])

        result = _find_n_numbers_summing_to_helper(numbers, n - 1, target, i, new_numbers_to_examine)

        if result != None:
            return result

    return None