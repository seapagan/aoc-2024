"""AOC 2024 - Day 7: Bridge Repair."""

from __future__ import annotations

import time
from functools import wraps
from itertools import product
from pathlib import Path
from typing import Iterable


def timer(func):
    """Decorator to measure the execution time of a function in milliseconds."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000
        print(f"{func.__name__}() took {elapsed_time_ms:.3f} ms")
        return result

    return wrapper


@timer
def get_data() -> Iterable[tuple[int, list[int]]]:
    """
    Process the input file and return a list of tuples:
    Each tuple contains:
        - An integer (test value)
        - A list of integers (operators)

    This could be done with a generator instead to reduce memory usage, but
    since it is needed in part2 as well we would have to regenerate it, and that
    would cost twice the disk access time.
    """
    with Path("./input.txt").open() as file:
        return [
            (
                int(line_parts[0][:-1]),  # Test value (remove trailing colon)
                list(map(int, line_parts[1:])),  # List of operators
            )
            for line in file
            if (line_parts := line.strip().split(" "))
        ]


def evaluate_expression(numbers: list[int], operators: Iterable[str]) -> int:
    """
    Evaluate an expression left-to-right given numbers and operators.
    Numbers and operators must be of compatible lengths: len(numbers) == len(operators) + 1.
    Supports +, *, and || operators.
    """
    result = numbers[0]
    for num, op in zip(numbers[1:], operators):
        if op == "+":
            result += num
        elif op == "*":
            result *= num
        elif op == "||":
            result = int(str(result) + str(num))  # Concatenate digits
    return result


def is_valid_equation(target: int, numbers: list[int], operators: list[str]) -> bool:
    """
    Check if the target value can be produced by inserting the specified operators between numbers.
    """
    num_operators = len(numbers) - 1
    all_operator_combinations = product(operators, repeat=num_operators)

    for operator_combination in all_operator_combinations:
        if evaluate_expression(numbers, operator_combination) == target:
            return True
    return False


@timer
def part1(data: list[tuple[int, list[int]]]) -> int:
    """
    Solve Part 1 by determining the total of all valid test values using + and *.
    """
    total = 0
    for target, numbers in data:
        if is_valid_equation(target, numbers, ["+", "*"]):  # Only + and *
            total += target
    return total


@timer
def part2(data: list[tuple[int, list[int]]]) -> int:
    """
    Solve Part 2 by determining the total of all valid test values using +, *, and ||.
    """
    total = 0
    for target, numbers in data:
        if is_valid_equation(target, numbers, ["+", "*", "||"]):  # Include ||
            total += target
    return total


def main() -> None:
    """Run the AOC problems for Day 6."""
    data = get_data()

    # Part 1 - answer for me is 12940396350192
    result1 = part1(data)
    print(f"Part 1: The total calibration result is : {result1}")

    # Part 2 - answer for me is 106016735664498
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
