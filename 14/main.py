"""AOC 2024 - Day 14: Restroom Redoubt."""

from __future__ import annotations

import time
from collections import deque
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeAlias, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

# just a few type aliases to clarify the code a little
InputData: TypeAlias = list[tuple[int, int, int, int]]
Point: TypeAlias = tuple[int, int]
Neighbor = Point


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds.

    This is a decorator that can be added to any function.
    """

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
def get_data() -> InputData:
    """Process the input file, return list of (px, py, vx, vy)."""
    with Path("./input.txt").open() as file:
        processed_data: InputData = []
        for line in file:
            # Get position and velocity for each robot
            parts = line.strip().split()
            px, py = map(int, parts[0][2:].split(","))
            vx, vy = map(int, parts[1][2:].split(","))
            processed_data.append((px, py, vx, vy))
        return processed_data


@timer
def part1(data: InputData) -> int:
    """Solve Part 1."""
    width, height = 101, 103
    quadrants = [0, 0, 0, 0]

    for px, py, vx, vy in data:
        # Calculate final position after 100 seconds
        final_x = (px + 100 * vx) % width
        final_y = (py + 100 * vy) % height

        # Ignore robots on central lines
        if final_x == width // 2 or final_y == height // 2:
            continue

        if final_x < width // 2 and final_y < height // 2:
            quadrants[0] += 1
        elif final_x >= width // 2 and final_y < height // 2:
            quadrants[1] += 1
        elif final_x < width // 2 and final_y >= height // 2:
            quadrants[2] += 1
        else:
            quadrants[3] += 1

    safety_factor = 1
    for count in quadrants:
        safety_factor *= count

    return safety_factor


def build_neighbor_lookup(
    width: int, height: int
) -> dict[Point, list[Neighbor]]:
    """Precompute valid neighbors for all positions in the grid.

    This speeds up the flood-fill as it doesn't need to do the calcs itself.
    """
    neighbor_map = {}
    for y in range(height):
        for x in range(width):
            neighbor_map[(x, y)] = [
                (x + dx, y + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < width and 0 <= y + dy < height
            ]
    return neighbor_map


def get_largest_robot_cluster(
    positions: list[Point],
    width: int,
    height: int,
    neighbor_map: dict[Point, list[Neighbor]],
) -> int:
    """Find the size of the largest connected cluster of robots.

    Basically uses a flood fill wich we then compare to a threshold later. Works
    in this case as there is only one iteration where we have a decent block of
    robots (the tree).
    """
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for x, y in positions:
        grid[y][x] = 1

    visited = set()
    largest_cluster = 0

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1 and (x, y) not in visited:
                cluster_size = 0
                queue = deque([(x, y)])
                while queue:
                    cx, cy = queue.popleft()
                    if (cx, cy) in visited:
                        continue
                    visited.add((cx, cy))
                    cluster_size += 1

                    for nx, ny in neighbor_map[(cx, cy)]:
                        if grid[ny][nx] == 1 and (nx, ny) not in visited:
                            queue.append((nx, ny))

                largest_cluster = max(largest_cluster, cluster_size)

    return largest_cluster


@timer
def part2(data: InputData) -> int:
    """Solve Part 2."""
    width, height = 101, 103
    iteration_count = 0

    # compute all potential neighbors in the grid befor we start, this sped up
    # the 'get_largest_robot_cluster()' by about a second.
    neighbor_map = build_neighbor_lookup(width, height)

    while True:
        positions = [
            (
                (px + iteration_count * vx) % width,
                (py + iteration_count * vy) % height,
            )
            for px, py, vx, vy in data
        ]

        largest_cluster = get_largest_robot_cluster(
            positions, width, height, neighbor_map
        )

        if largest_cluster > 15:  # found by trial and error  # noqa: PLR2004
            # visualize_grid(positions)
            return iteration_count

        iteration_count += 1


def visualize_grid(
    positions: list[Point], width: int = 101, height: int = 103
) -> None:
    """Print the full grid.

    This was used during the tuning phase for visual confirmation. Prints a
    pretty output of the passed grid.
    """
    grid = [["." for _ in range(width)] for _ in range(height)]

    for x, y in positions:
        grid[y][x] = "#"

    for row in grid:
        print("".join(row))


@timer
def main() -> None:
    """Run the AOC problems for Day 14."""
    data = get_data()

    # Part 1 - answer for me is 218965032
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is 7037
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()

# ---------------------------------- timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : 0.326 ms
#    part1 : 0.069 ms
#    part2 : 2673.080 ms
#    Total : 2773.522 ms
