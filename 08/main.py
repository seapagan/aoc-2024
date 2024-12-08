"""AOC 2024 - Day 8: Resonant Collinearity."""

from __future__ import annotations

import time
from collections import defaultdict
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Callable, ParamSpec, TypeAlias, TypedDict, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

P = ParamSpec("P")
R = TypeVar("R")

Grid: TypeAlias = list[list[str]]
AntennaMap: TypeAlias = defaultdict[str, list[tuple[int, int]]]
Bounds: TypeAlias = tuple[int, int]


class DataDict(TypedDict):
    """Define typing for the get_data() function."""

    map: Grid
    antennas: AntennaMap
    bounds: Bounds


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
def get_data() -> DataDict:
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        grid: Grid = []
        antennas: AntennaMap = defaultdict(list)

        for line_index, line in enumerate(file):
            stripped_line = line.strip()
            this_line = []
            for pos_index, position in enumerate(stripped_line):
                if position != ".":
                    antennas[position].append((line_index, pos_index))
                this_line.append(position)
            grid.append(this_line)

    bounds: Bounds = len(grid), len(grid[0])

    return {"map": grid, "antennas": antennas, "bounds": bounds}


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
    """Run the AOC problems for Day 8."""
    data = get_data()

    print(data)

    # Part 1 - answer for me is ?
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
