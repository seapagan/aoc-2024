"""AOC 2024 - Day 16: Reindeer Maze."""

from __future__ import annotations

import time
from functools import wraps
from heapq import heappop, heappush
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeAlias, TypeVar

from rich import box
from rich.console import Console
from rich.table import Table

Point: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[list[str]]

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

timing_results = []


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000
        timing_results.append((func.__name__, elapsed_time_ms))
        return result

    return wrapper


def print_timings() -> None:
    """Pretty-print the timing results for all decorated functions."""
    console = Console()
    table = Table(show_header=False, title="Timing Results", box=box.ROUNDED)

    table.add_column(justify="left", style="cyan", no_wrap=True)
    table.add_column(justify="right", style="green")

    for idx, (func_name, elapsed_time) in enumerate(timing_results):
        is_last = idx == len(timing_results) - 1
        is_second_to_last = idx == len(timing_results) - 2

        display_name = (
            "Total Runtime" if is_last and func_name == "main" else func_name
        )

        table.add_row(
            display_name,
            f"{elapsed_time:.3f}",
            end_section=is_second_to_last and timing_results[-1][0] == "main",
        )

    console.print()
    console.print(table, style="grey50")


@timer
def get_data() -> tuple[Grid, Point, Point]:
    """Parse the input file, returning the maze grid and start/end positions."""
    with Path("./input.txt").open() as file:
        grid = [list(line.strip()) for line in file]

    start, end = None, None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            elif cell == "E":
                end = (r, c)

    if not start or not end:
        error_msg = "Maze must contain both a start (S) and end (E)."
        raise ValueError(error_msg)

    return grid, start, end


@timer
def part1(
    data: tuple[Grid, Point, Point],
) -> int:
    """Solve Part 1.

    Doing this with a UCS (Uniform-Cost Search). Tried using A* but was
    actaully slightly slower in this case. This whole function could prob be
    optimized more too.
    """
    grid, start, end = data
    directions = {"E": (0, 1), "S": (1, 0), "W": (0, -1), "N": (-1, 0)}
    rotations = {
        "E": ["N", "S"],
        "S": ["E", "W"],
        "W": ["S", "N"],
        "N": ["W", "E"],
    }

    # Priority queue: (cost, x, y, direction)
    pq = [(0, *start, "E")]
    visited: set[tuple[int, int, str]] = set()

    while pq:
        cost, x, y, direction = heappop(pq)

        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        if (x, y) == end:
            return cost

        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < len(grid)
            and 0 <= ny < len(grid[0])
            and grid[nx][ny] != "#"
        ):
            heappush(pq, (cost + 1, nx, ny, direction))

        # Rotate clockwise or counterclockwise
        for new_dir in rotations[direction]:
            heappush(pq, (cost + 1000, x, y, new_dir))

    return 0  # can't find a good path. Just here to stop Ruff complaining!


@timer
def part2(
    data: tuple[Grid, Point, Point],
) -> int:
    """Solve Part 2."""
    total = 0

    return total


@timer
def main() -> None:
    """Run the AOC problems for Day 16."""
    data = get_data()

    # Part 1 - answer for me is 72428
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
    print_timings()

# ---------------------------------- Timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : x.xxx ms
#    part1 : x.xxx ms
#    part2 : x.xxx ms
#    Total : x.xxx ms
