"""AOC 2024 - Day 14: Restroom Redoubt."""

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
def get_data() -> list[tuple[int, int, int, int]]:
    """Process the input file, return list of (px, py, vx, vy)."""
    with Path("./input.txt").open() as file:
        processed_data = []
        for line in file:
            # Get position and velocity for each robot
            parts = line.strip().split()
            px, py = map(int, parts[0][2:].split(","))
            vx, vy = map(int, parts[1][2:].split(","))
            processed_data.append((px, py, vx, vy))
        return processed_data


@timer
def part1(data: list[tuple[int, int, int, int]]) -> int:
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


@timer
def part2(
    data: list[tuple[int, int, int, int]],
) -> int:
    """Solve Part 2."""
    total = 0

    return total


@timer
def main() -> None:
    """Run the AOC problems for Day 14."""
    data = get_data()

    # Part 1 - answer for me is 218965032
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 - answer for me is ?
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()

# ---------------------------------- timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : 0.327 ms
#    part1 : 0.070 ms
#    part2 : x.xxx ms
#    Total : x.xxx ms
