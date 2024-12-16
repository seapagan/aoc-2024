"""AOC 2024 - Day 15: Warehouse Woes."""

from __future__ import annotations

import sys
import time
from collections import defaultdict
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, ParamSpec, TypeAlias, TypeVar

from rich import box
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

InputData: TypeAlias = tuple[list[str], str]
Point: TypeAlias = tuple[int, int]
Grid: TypeAlias = defaultdict[Point, str]

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
            f"{elapsed_time:.3f} ms",
            end_section=is_second_to_last and timing_results[-1][0] == "main",
        )

    console.print()
    console.print(table, style="grey50")


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
    data: InputData,
) -> int:
    """Solve Part 2."""

    def create_grid(
        raw_grid: list[str],
    ) -> tuple[Grid, Point | None]:
        """Return a scaled grid we can work on."""
        grid: Grid = defaultdict(lambda: "#")
        start = None

        scale_mappings: dict[str, str] = {
            "O": "[]",
            ".": "..",
            "#": "##",
            "@": "@.",
        }

        scaled_grid = [
            "".join(scale_mappings.get(char, char) for char in line)
            for line in raw_grid
        ]

        # Build the final grid
        for row, line in enumerate(scaled_grid):
            for col, tile in enumerate(line):
                grid[(row, col)] = tile
                if tile == "@":
                    start = (row, col)
        return grid, start

    def get_move_offset(symbol: str) -> tuple[int, int]:
        """Return tuple with offset for the given move symbol."""
        return {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}[symbol]

    def get_next_position(position: Point, move: Point) -> Point:
        """Return the next position after a move."""
        return (position[0] + move[0], position[1] + move[1])

    def can_we_move(
        box_position: Point,
        move: Point,
        boxes: set[Point],
        grid: Grid,
    ) -> bool:
        checked: set[Point] = set()
        box_sides = {"[": get_move_offset(">"), "]": get_move_offset("<")}

        if grid[box_position] in box_sides:
            checked = {
                box_position,
                get_next_position(box_position, box_sides[grid[box_position]]),
            }

        new_positions = {get_next_position(p, move) for p in checked} - checked

        if any(grid[p] == "#" for p in new_positions):
            return False

        valid = all(
            grid[p] == "." or can_we_move(p, move, boxes, grid)
            for p in new_positions
        )

        if valid:
            for c in checked:
                boxes.add(c)
            return valid

        return False

    raw_grid, raw_moves = data
    grid, start_point = create_grid(raw_grid)

    if not start_point:
        print("Cant find the robot!!")
        sys.exit(1)

    current_location = start_point
    moves = [get_move_offset(d) for d in raw_moves]

    for move in moves:
        new_pos = get_next_position(current_location, move)

        if grid[new_pos] == "#":
            continue

        if grid[new_pos] == ".":
            grid[new_pos], grid[current_location] = "@", "."
            current_location = new_pos
            continue

        if grid[new_pos] in "[]":
            boxes: set[Point] = set()
            if not can_we_move(new_pos, move, boxes, grid):
                continue

            new_grid: dict[Point, str] = {}
            for box_pos in boxes:
                new_grid[get_next_position(box_pos, move)] = grid[box_pos]
                grid[box_pos] = "."
            for box_pos, contents in new_grid.items():
                grid[box_pos] = contents

            grid[new_pos], grid[current_location] = "@", "."
            current_location = new_pos

    box_positions = [
        (row, col) for (row, col) in grid if grid[(row, col)] == "["
    ]
    return sum(100 * row + col for row, col in box_positions)


@timer
def main() -> None:
    """Run the AOC problems for Day 15."""
    data = get_data()

    # Part 1 - answer for me is 1451928
    result1 = part1(data)
    print(f"Part 1: The sum of all the box GPS coordinates is {result1}")

    # Part 2 - answer for me is 1462788
    result2 = part2(data)
    print(f"Part 2: The sum of the Scaled-up box GPS coordinates is {result2}")


if __name__ == "__main__":
    main()
    print_timings()

# ---------------------------------- Timings --------------------------------- #
# ------------- Run on an i7-14700K with SSD and DDR5-6000 memory ------------ #
# ------------------------------- Python 3.13.1 ------------------------------ #
# ---------------------------------------------------------------------------- #
# get_data : 0.057 ms
#    part1 : 2.844 ms
#    part2 : 15.417 ms
#    Total : 18.339 ms
