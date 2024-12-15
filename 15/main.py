"""AOC 2024 - Day 15: Warehouse Woes."""

from __future__ import annotations

import time
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000
        print(
            f"\nTotal Runtime was {elapsed_time_ms:.3f} ms"
            if func.__name__ == "main"
            else f"[ {func.__name__}() took {elapsed_time_ms:.3f} ms ]"
        )
        return result

    return wrapper


@timer
def get_data() -> list[str]:
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        return file.readlines()


@timer
def part1(
    data: list[str],
) -> int:
    """Solve Part 1."""
    total = 0

    return total


@timer
def part2(
    data: list[str],
) -> int:
    """Solve Part 2."""
    total = 0

    return total


def main() -> None:
    """Run the AOC problems for Day 15."""
    data = get_data()

    # Part 1 - answer for me is ?
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()

# ---------------------------------- Timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : x.xxx ms
#    part1 : x.xxx ms
#    part2 : x.xxx ms
#    Total : x.xxx ms
