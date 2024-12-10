"""AOC 2024 - Day 10: Hoof It."""

from __future__ import annotations

import time
from collections import deque
from functools import lru_cache, wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

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


def bfs(grid: list[list[int]], start: tuple[int, int]) -> int:
    """Perform BFS from a trailhead and count reachable height 9 positions."""
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set()
    visited.add(start)
    valid_trails = set()

    while queue:
        row, col = queue.popleft()
        for dr, dc in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:  # Up, down, left, right
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and (nr, nc) not in visited
                and grid[nr][nc] == grid[row][col] + 1
            ):
                if grid[nr][nc] == END_OF_TRAIL:
                    valid_trails.add((nr, nc))
                queue.append((nr, nc))
                visited.add((nr, nc))

    return len(valid_trails)


@timer
def part1(data: list[list[int]]) -> int:
    """Solve Part 1."""
    ratings_sum = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == 0:  # Found a trailhead
                ratings_sum += bfs(data, (row, col))
    return ratings_sum


def count_paths_from(grid: list[list[int]], start: tuple[int, int]) -> int:
    """Count the number of distinct trails starting from a given position."""
    rows, cols = len(grid), len(grid[0])

    @lru_cache(None)
    def dfs(row: int, col: int) -> int:
        # Base case: Reached height 9
        if grid[row][col] == END_OF_TRAIL:
            return 1

        # Count paths from valid neighbors
        total_paths = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == grid[row][col] + 1  # Valid uphill step
            ):
                total_paths += dfs(nr, nc)

        return total_paths

    return dfs(*start)


@timer
def part2(data: list[list[int]]) -> int:
    """Solve Part 2."""
    ratings_sum = 0
    rows, cols = len(data), len(data[0])

    # Iterate over all trailheads (height 0) and calculate their ratings
    for row in range(rows):
        for col in range(cols):
            if data[row][col] == 0:  # Found a trailhead
                ratings_sum += count_paths_from(data, (row, col))

    return ratings_sum


def main() -> None:
    """Run the AOC problems for Day 10."""
    data = get_data()

    # Part 1 - answer for me is 717
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is 1686
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
