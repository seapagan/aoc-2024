"""AOC 2024 - Day 12: Garden Groups."""

from __future__ import annotations

import time
from collections import deque
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

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
        return [line.strip() for line in file if line.strip()]


@timer
def part1(grid: list[str]) -> int:
    """Solve Part1, using the perimeter."""
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def neighbors(r: int, c: int) -> Generator[tuple[int, int]]:
        yield from [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    total_price = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                # New region
                char = grid[r][c]
                queue = deque([(r, c)])
                visited[r][c] = True
                area = 0
                perimeter = 0

                while queue:
                    cr, cc = queue.popleft()
                    area += 1
                    for nr, nc in neighbors(cr, cc):
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == char:
                                if not visited[nr][nc]:
                                    visited[nr][nc] = True
                                    queue.append((nr, nc))
                            else:
                                perimeter += 1
                        else:
                            perimeter += 1

                # Calculate price for the region
                price = area * perimeter
                total_price += price

    return total_price


def part2(grid: list[str]) -> int:
    total_price = 0

    return total_price


def main() -> None:
    """Run the AOC problems for Day 12."""
    data = get_data()

    # Part 1 - answer for me is 1485656
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
