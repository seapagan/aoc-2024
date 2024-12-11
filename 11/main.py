"""AOC 2024 - Day 11: Plutonian Pebbles."""

from __future__ import annotations

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
def get_data() -> list[str]:
    """Process the input file, return in a suitable format.

    For this puzzle, a simple list of each initiaal pebble as a string is ok.
    """
    with Path("./input.txt").open() as file:
        line = file.readline().strip()
    return line.split()


def transform_stone(stone: str) -> list[str]:
    """Transforn the given stone using the rules."""
    if stone == "0":
        return ["1"]

    length = len(stone)
    if length % 2 == 0:
        # Even length: split into two stones with no leading zeros
        half = length // 2
        left = stone[:half].lstrip("0") or "0"
        right = stone[half:].lstrip("0") or "0"
        return [left, right]

    # Odd length: multiply by 2024
    val = int(stone) * 2024
    return [str(val)]


@cache
def get_final_stone_count(stone: str, t: int) -> int:
    """Return the # of stones from a single stone after 't' blinks."""
    if t == 0:
        return 1
    transformed = transform_stone(stone)
    total = 0
    for s in transformed:
        total += get_final_stone_count(s, t - 1)
    return total


@timer
def part1(data: list[str]) -> int:
    """Get the result after 25 blinks."""
    t = 25
    return sum(get_final_stone_count(stone, t) for stone in data)


@timer
def part2(data: list[str]) -> int:
    """Get the result after 75 blinks."""
    t = 75
    return sum(get_final_stone_count(stone, t) for stone in data)


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
# ---------------------------------------------------------------------------- #
# get_data : 0.032 ms
#    part1 : 1.762 ms
#    part2 : 57.200 ms
#    Total : 59.033 ms
