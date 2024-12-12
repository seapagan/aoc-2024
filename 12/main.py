"""AOC 2024 - Day 12: Garden Groups."""

from __future__ import annotations

import time
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeAlias, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

Point: TypeAlias = tuple[int, int]


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
def get_data(filename: str) -> list[str]:
    """Get the data and put into a suitable format."""
    with Path(filename).open() as file:
        return file.read().strip().split("\n")


def is_pos_in_grid(grid: list[str], pos: Point) -> bool:
    """Return True if pos is inside the given grid."""
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def dfs(visited: set[Point], grid: list[str], pos: Point) -> set[Point]:
    """DFS search to find all nodes reachable from given pos."""
    if pos not in visited:
        visited.add(pos)
        x, y = pos
        for dx, dy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if is_pos_in_grid(grid, (dx, dy)) and grid[dy][dx] == grid[y][x]:
                dfs(visited, grid, (dx, dy))
    return visited


def count_shared_sides(region: set[Point]) -> int:
    """Count shared sides between points in a grid region."""
    count = 0
    for x, y in region:
        if (x - 1, y) in region:
            for y2 in [y - 1, y + 1]:
                if (x, y2) not in region and (x - 1, y2) not in region:
                    count += 1
        if (x, y - 1) in region:
            for x2 in [x - 1, x + 1]:
                if (x2, y) not in region and (x2, y - 1) not in region:
                    count += 1
    return count


@timer
def solve(grid: list[str]) -> tuple[int, int]:
    """Solve both parts at once."""
    total_cost = 0
    discounted_cost = 0
    already_visited: set[Point] = set()
    regions: list[set[Point]] = []

    for y, line in enumerate(grid):
        for x in range(len(line)):
            pos = (x, y)
            if pos in already_visited:
                continue

            region = dfs(set(), grid, pos)
            area = len(region)
            perimeter = sum(
                4
                - sum(
                    1
                    for nx, ny in (
                        (x + 1, y),
                        (x - 1, y),
                        (x, y + 1),
                        (x, y - 1),
                    )
                    if (nx, ny) in region
                )
                for x, y in region
            )
            total_cost += area * perimeter
            discounted_cost += area * (perimeter - count_shared_sides(region))
            already_visited.update(region)
            regions.append(region)
    return total_cost, discounted_cost


@timer
def main() -> None:
    """Solve Day 12."""
    grid = get_data("input.txt")

    part1, part2 = solve(grid)

    print(f"Part 1: Pricing using area is {part1}")  # answer for me is 1485656
    print(
        f"Part 2: Discounted pricing using sides is {part2}"
    )  # answer for me is 899196


if __name__ == "__main__":
    main()

# ---------------------------------- timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data :  0.055 ms
#    solve : 26.502 ms
#    Total : 26.582 ms
