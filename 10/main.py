"""AOC 2024 - Day 10: Hoof It."""

from __future__ import annotations

import time
from functools import lru_cache, wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

END_OF_TRAIL = 9


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
def get_data() -> list[list[int]]:
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        return [[int(char) for char in line.strip()] for line in file]


def process_trail(
    grid: list[list[int]], start: tuple[int, int]
) -> tuple[int, int]:
    """Process one trailhead for both puzzle parts simultaneously."""
    rows, cols = len(grid), len(grid[0])
    valid_trails = set()

    @lru_cache(None)
    def explore(row: int, col: int) -> int:
        if grid[row][col] == END_OF_TRAIL:
            valid_trails.add((row, col))  # Track unique reachable 9s
            return 1  # path ends here

        total_paths = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == grid[row][col] + 1
            ):
                total_paths += explore(
                    nr, nc
                )  # Accumulate paths from neighbors

        return total_paths

    total_trails = explore(*start)
    return len(valid_trails), total_trails  # Part 1 result, Part 2 result


@timer
def solve(data: list[list[int]]) -> tuple[int, int]:
    """Solve both Part 1 and Part 2 simultaneously."""
    part1_sum = 0
    part2_sum = 0
    rows, cols = len(data), len(data[0])

    for row in range(rows):
        for col in range(cols):
            if data[row][col] == 0:  # Found a trailhead
                part1, part2 = process_trail(data, (row, col))
                part1_sum += part1
                part2_sum += part2

    return part1_sum, part2_sum


@timer
def main() -> None:
    """Run the AOC problems for Day 10."""
    data = get_data()

    part1_result, part2_result = solve(data)
    print(
        f"Part 1: Sum of all trialhead scores is {part1_result}"
    )  # 717 for me
    print(
        f"Part 2: Sum of all trailhead ratings is {part2_result}"
    )  # 1686 for me


if __name__ == "__main__":
    main()

# ---------------------------------- timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ---------------------------------------------------------------------------- #
# get_data() : 0.170 ms
#    solve() : 2.329 ms
#     Total : 2.514 ms
