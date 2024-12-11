"""AOC 2024 - Day 11: Plutonian Pebbles.

This is re-written to use integer maths, since the numbers are small enough, and
it drops about 8-10ms on the runtime. This may fail with a different data set
though.
"""

from __future__ import annotations

import math
import time
from functools import cache, wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds.

    This is a decorator that can be added to any function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000
        print(f"{func.__name__}() took {elapsed_time_ms:.3f} ms")
        return result

    return wrapper


@timer
def get_data() -> list[int]:
    """Process the input file, return in a suitable format.

    For this puzzle, a simple list of each initial pebble as an int.
    """
    with Path("./input.txt").open() as file:
        line = file.readline().strip()
    return [int(x) for x in line.split()]


def transform_stone(stone: int) -> list[int]:
    """Transform the given stone using the rules."""
    if stone == 0:
        # If the stone is 0, it becomes 1
        return [1]

    # Determine the number of digits of the stone
    length = int(math.log10(stone)) + 1

    if length % 2 == 0:
        # Even number of digits: split into two stones
        half = length // 2
        power_of_10 = 10**half

        left = stone // power_of_10
        right = stone % power_of_10
        return [left, right]

    # Odd number of digits: multiply by 2024
    return [stone * 2024]


@cache
def get_final_stone_count(stone: int, t: int) -> int:
    """Return the # of stones from a single stone after 't' blinks."""
    if t == 0:
        return 1
    transformed = transform_stone(stone)
    total = 0
    for s in transformed:
        total += get_final_stone_count(s, t - 1)
    return total


@timer
def part1(data: list[int]) -> int:
    """Get the result after 25 blinks."""
    return sum(get_final_stone_count(stone, 25) for stone in data)


@timer
def part2(data: list[int]) -> int:
    """Get the result after 75 blinks."""
    return sum(get_final_stone_count(stone, 75) for stone in data)


@timer
def main() -> None:
    """Run the AOC problem for Day 11."""
    data = get_data()

    # Part 1 for me is 183248
    result1 = part1(data)
    print(f"Part 1: After 25 blinks we have {result1} stones!")

    # Part 2 for me is 218811774248729
    result2 = part2(data)
    print(f"Part 2: After 75 blinks we have an astonishing {result2} stones!")


if __name__ == "__main__":
    main()

# ---------------------------------- timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : 0.044 ms
#    part1 : 1.470 ms
#    part2 : 48.340 ms
#    Total : 49.896 ms
