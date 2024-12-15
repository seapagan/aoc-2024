"""AOC 2024 - Day 15: Warehouse Woes."""

from __future__ import annotations

import sys
import time
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeAlias, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

InputData: TypeAlias = tuple[list[str], str]
Point: TypeAlias = tuple[int, int]


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
def get_data() -> InputData:
    """Process the input file, return in a suitable format."""
    with Path("./input.txt").open() as file:
        warehouse, moves = file.read().split("\n\n")

    grid = warehouse.split("\n")
    moves = moves.replace("\n", "")

    return grid, moves


@timer
def part1(data: InputData) -> int:
    """Solve Part 1."""
    grid, moves = data

    walls: set[Point] = set()
    boxes: set[Point] = set()
    robot = None

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == "#":
                walls.add((r, c))
            elif char == "O":
                boxes.add((r, c))
            elif char == "@":
                robot = (r, c)

    if not robot:
        print("Cannot find the Robot, exiting!")
        sys.exit(1)

    directions: dict[str, Point] = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    def is_valid_point(position: Point) -> bool:
        return position not in walls and position not in boxes

    for move in moves:
        dr, dc = directions[move]
        next_position = (robot[0] + dr, robot[1] + dc)

        if next_position in boxes:
            box_chain = []
            current = next_position
            while current in boxes:
                box_chain.append(current)
                current = (current[0] + dr, current[1] + dc)

            if is_valid_point(current):
                for box in reversed(box_chain):
                    boxes.remove(box)
                    boxes.add((box[0] + dr, box[1] + dc))
                robot = next_position
        elif is_valid_point(next_position):
            robot = next_position

    # Calculate the GPS sum for all boxes
    gps_sum = 0
    for r, c in boxes:
        gps_sum += 100 * r + c

    return gps_sum


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

    # Part 1 - answer for me is 1451928
    result1 = part1(data)
    print(f"Part 1: The sum of all the box GPS coordinatese is {result1}")

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
