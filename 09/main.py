"""AOC 2024 - Day 9: Disk Fragmenter."""

from __future__ import annotations

import time
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

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
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        # return [
        #     (
        #         int(line_parts[0][:-1]),  # Test value (remove trailing colon)
        #         list(map(int, line_parts[1:])),  # List of operators
        #     )
        #     for line in file
        #     if (line_parts := line.strip().split(" "))
        # ]
        return file.readlines()


@timer
def part1(
    data: Iterable[str],
) -> int:
    """Solve Part 1."""
    total = 0

    return total


@timer
def part2(
    data: Iterable[str],
) -> int:
    """Solve Part 2."""
    total = 0

    return total


def main() -> None:
    """Run the AOC problems for Day 9."""
    data = get_data()

    # Part 1 - answer for me is ?
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
