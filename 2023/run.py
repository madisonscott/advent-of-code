import importlib
import importlib.machinery
import os
from pathlib import Path
import shutil
import sys

input_dir_path = 'input'

def day_solver_filepath(day):
    return f'{day}.py'

def day_input_filepath(day):
    return os.path.join(input_dir_path, f'{day}.txt')

def create_day(day):
    solver_filepath = day_solver_filepath(day)
    if not os.path.exists(solver_filepath):
        shutil.copy('template.py', solver_filepath)
        print(f'Created {solver_filepath} from template')

    if not os.path.exists(input_dir_path):
        os.mkdir(input_dir_path)

    input_filepath = day_input_filepath(day)
    if not os.path.exists(input_filepath):
        Path(input_filepath).touch()
        print(f'Created {input_filepath}')


def load_from_file(filepath, expected_class):
    mod_name = Path(filepath).stem
    loader = importlib.machinery.SourceFileLoader(mod_name, filepath)
    module = loader.load_module()

    # https://stackoverflow.com/a/301298
    if not hasattr(module, expected_class):
        raise Exception(f'Could not find {expected_class} in {filepath}')

    return getattr(module, expected_class)()

def main():
    args = sys.argv[1:]
    day = args[args.index('-d') + 1]
    should_create = '--create' in args

    if should_create:
        create_day(day)
        return

    input = ''
    solver = load_from_file(day_solver_filepath(day), 'Solver')

    part = int(args[args.index('-p') + 1])
    should_test = '--test' in args

    if should_test:
        input = solver.test_input_one() if part == 1 else solver.test_input_two()
    else:
        with open(day_input_filepath(day)) as f:
            input = f.read()

    if part == 1:
        print(solver.solve_part_one(input))
    elif part == 2:
        print(solver.solve_part_two(input))

if __name__ == '__main__':
    main()
